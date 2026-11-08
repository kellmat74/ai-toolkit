#Requires -Version 7.0
<#
.SYNOPSIS
  Windows counterpart of setup.sh: symlinks ai-toolkit into %USERPROFILE%\.claude
  (and optionally Hermes). Idempotent and safe to re-run.

.DESCRIPTION
  - Only ever replaces something that is already a symlink. A real file or
    directory at the destination is left alone and reported.
  - Needs Windows Developer Mode (or an elevated shell) so symlinks can be
    created. Windows PowerShell 5.1 cannot create unprivileged symlinks, which
    is why this script requires PowerShell 7 (pwsh).
  - Never falls back to copying. If a link cannot be created it says so and
    moves on, because a copy would stop edits landing in git.
  - Skips Codex, the MCP render and Hermes unless asked. The MCP render is a
    separate step: python claude\restore-mcp-config.py

.PARAMETER Hermes
  Also link hermes\config.yaml and hermes\skills\* into the Hermes home
  ($env:HERMES_HOME, else %LOCALAPPDATA%\hermes). Off by default.

.PARAMETER DryRun
  Print what would happen without changing anything.
#>
[CmdletBinding()]
param(
    [switch]$Hermes,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$Repo = $PSScriptRoot
$ClaudeHome = Join-Path $HOME '.claude'
$HermesHome = if ($env:HERMES_HOME) { $env:HERMES_HOME } else { Join-Path $env:LOCALAPPDATA 'hermes' }

$script:Linked = 0
$script:Unchanged = 0
$script:Skipped = 0
$script:Failed = 0

Write-Host "Wiring ai-toolkit from: $Repo"
if ($DryRun) { Write-Host '(dry run, nothing will change)' }

function Ensure-Dir([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        if ($DryRun) { Write-Host "  would create $Path"; return }
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Get-LinkTarget([string]$Path) {
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) { return $null }
    if ($item.LinkType -ne 'SymbolicLink') { return $null }
    return ($item.Target | Select-Object -First 1)
}

function Link-Item([string]$Source, [string]$Dest) {
    if (-not (Test-Path -LiteralPath $Source)) { return }

    $existing = Get-Item -LiteralPath $Dest -Force -ErrorAction SilentlyContinue
    if ($null -ne $existing) {
        if ($existing.LinkType -ne 'SymbolicLink') {
            Write-Host "  SKIP $Dest exists and is a real file or directory, not touching it" -ForegroundColor Yellow
            $script:Skipped++
            return
        }
        $current = Get-LinkTarget $Dest
        if ($current -and ((Resolve-Path -LiteralPath $current -ErrorAction SilentlyContinue).Path -eq (Resolve-Path -LiteralPath $Source).Path)) {
            Write-Host "  ok   $Dest"
            $script:Unchanged++
            return
        }
        if ($DryRun) { Write-Host "  would relink $Dest -> $Source"; return }
        $existing.Delete()   # removes the link only, never the target
    }

    if ($DryRun) { Write-Host "  would link $Dest -> $Source"; return }
    try {
        New-Item -ItemType SymbolicLink -Path $Dest -Target $Source -ErrorAction Stop | Out-Null
        Write-Host "  linked $Dest -> $Source"
        $script:Linked++
    }
    catch {
        Write-Host "  FAIL $Dest : $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "       Is Developer Mode on? (Settings, System, For developers)" -ForegroundColor Red
        $script:Failed++
    }
}

# ---------- Claude Code ----------
Write-Host "`n[Claude Code] -> $ClaudeHome"
foreach ($d in 'skills', 'agents', 'commands') { Ensure-Dir (Join-Path $ClaudeHome $d) }

foreach ($f in 'CLAUDE.md', 'settings.json', 'keybindings.json') {
    Link-Item (Join-Path $Repo "claude\$f") (Join-Path $ClaudeHome $f)
}

foreach ($d in 'skills', 'agents', 'commands') {
    $srcDir = Join-Path $Repo "claude\$d"
    if (-not (Test-Path -LiteralPath $srcDir)) { continue }
    foreach ($entry in Get-ChildItem -LiteralPath $srcDir -Force) {
        if ($entry.Name -eq 'README.md') { continue }
        Link-Item $entry.FullName (Join-Path $ClaudeHome "$d\$($entry.Name)")
    }
}

# ---------- Hermes (opt-in) ----------
if ($Hermes) {
    Write-Host "`n[Hermes] -> $HermesHome"
    Ensure-Dir (Join-Path $HermesHome 'skills')
    Link-Item (Join-Path $Repo 'hermes\config.yaml') (Join-Path $HermesHome 'config.yaml')
    $hs = Join-Path $Repo 'hermes\skills'
    if (Test-Path -LiteralPath $hs) {
        foreach ($entry in Get-ChildItem -LiteralPath $hs -Force) {
            Link-Item $entry.FullName (Join-Path $HermesHome "skills\$($entry.Name)")
        }
    }
}
else {
    Write-Host "`n[Hermes] skipped (pass -Hermes to link it)"
}

Write-Host "`n[Codex] skipped on Windows"
Write-Host "[MCP]   not rendered here. Run: python claude\restore-mcp-config.py"

# ---------- Secrets check ----------
Write-Host ''
$missing = @()
if (-not (Test-Path (Join-Path $ClaudeHome '.env'))) { $missing += (Join-Path $ClaudeHome '.env') }
if ($Hermes -and -not (Test-Path (Join-Path $HermesHome '.env'))) { $missing += (Join-Path $HermesHome '.env') }
if (-not (Test-Path (Join-Path $ClaudeHome 'secrets.json'))) { $missing += (Join-Path $ClaudeHome 'secrets.json') }

if ($missing.Count -gt 0) {
    Write-Host 'Next: create these yourself, using .env.example as the guide (never commit them):'
    $missing | ForEach-Object { Write-Host "  - $_" }
    Write-Host 'Use credentials you OWN (personal keys and tokens).'
}
else {
    Write-Host 'Secrets files present.'
}

Write-Host "`nSummary: linked=$script:Linked unchanged=$script:Unchanged skipped=$script:Skipped failed=$script:Failed"
if ($script:Failed -gt 0) { exit 1 }
