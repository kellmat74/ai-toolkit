---
name: generate-image
description: Generate an image from this Claude Code surface using Seedream 4.5 via OpenRouter. Defaults to a fast direct API call; can optionally route through the local Hermes agent for async/scheduled work. Use when the user asks to generate, create, draw, or make an image, picture, illustration, or logo.
---

# Generate an image (Seedream 4.5)

Claude Code has no native image generation, but it CAN call an image API as a tool
action (a plain HTTPS request -- this is NOT blocked by the "Claude runs on Anthropic
models only" restriction, which governs the reasoning model, not outbound API calls).

**Two paths:**
- **Direct (default, ~30s):** Claude Code calls OpenRouter itself. Fast. Use this
  unless the user specifically wants the Hermes route.
- **Via Hermes (~2-4 min):** route through the local Hermes agent's `seedream` skill.
  Use only when the user asks for it, or when the image gen should run on the same
  async/scheduled path Hermes uses (Discord/cron). See the "Hermes route" section.

**Cost:** $0.04 per image (Seedream 4.5, fixed). Each successful call bills once. A
"no image" response may still have billed -- read the output before retrying.

## Direct path (default)

1. Use the user's description as the prompt verbatim. If it's a bare request ("a
   logo"), ask one quick clarifying question rather than inventing details.

2. Run this script (substitute `PROMPT`). It reads the key from `~/.hermes/.env` and
   verifies TLS against the Hermes CA bundle (TLS is intercepted on this Mac; plain
   certs fail with misleading errors):

```bash
python3 - <<'PY'
import json, os, ssl, time, base64, urllib.request

PROMPT = "<PROMPT HERE>"

key = os.environ.get("OPENROUTER_API_KEY", "")
if not key:
    p = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY=") and not line.startswith("#"):
                key = line.split("=", 1)[1].strip(); break
assert key, "OPENROUTER_API_KEY not found in env or ~/.hermes/.env"

bundle = os.path.expanduser("~/.hermes/certs/combined_ca_bundle.pem")
ctx = ssl.create_default_context(cafile=bundle) if os.path.exists(bundle) \
    else ssl.create_default_context()

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps({
        "model": "bytedance-seed/seedream-4.5",
        "messages": [{"role": "user", "content": PROMPT}],
        "modalities": ["image"],
    }).encode(),
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
             "HTTP-Referer": "https://claude.ai/code", "X-Title": "Claude Code"},
)
with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
    data = json.loads(r.read())

msg = data["choices"][0]["message"]
url = (msg.get("images") or [{}])[0].get("image_url", {}).get("url")
if not url:
    print("NO IMAGE (may still be billed):", json.dumps(data)[:800]); raise SystemExit(1)

ext = url.split("/", 1)[1].split(";", 1)[0] if url.startswith("data:image/") else "jpg"
out = f"/tmp/claude_genimg_{int(time.time())}.{ext}"
open(out, "wb").write(base64.b64decode(url.split(",", 1)[1]))
print(f"SAVED:{out}  COST:${data.get('usage', {}).get('cost')}")
PY
```

3. **Surface it.** Parse `SAVED:<path>` and sanity-check with `file <path>` (expect
   "JPEG/PNG image data" with dimensions). Then make it visible:
   - **`open <path>`** -- this is the reliable way on this surface. The Claude Code
     Mac app does NOT render images inline in the transcript; it only shows
     `SendUserFile` deliveries as clickable attachments. `open` pops the image in
     Preview immediately, which is what the user actually wants.
   - Also call `SendUserFile` (status `normal`, captioned with the prompt) so the
     file is attached to the conversation for later reference.
   State the cost and path; note `/tmp` clears on reboot.

## Hermes route (opt-in: async / scheduled / "do it through Hermes")

Drive Hermes to run its own `seedream` skill. Slower (full agent spin-up), but runs
on the same path as Discord/cron work. Run as a BACKGROUND task -- `--cli` only
flushes output on completion (see the `driving-hermes` skill):

```bash
REPO=~/git/personal/ai-toolkit
OUT=/tmp/claude_genimg_$(date +%s).jpg
hermes --cli --skills "$REPO/hermes/skills" -z "Use the seedream skill to generate \
an image. Prompt: <PROMPT>. Save to exactly $OUT and print one final line: \
SAVED:$OUT . Do not rename the file." 2>&1 | tee /tmp/hermes_genimg.log
```

Then parse `SAVED:<path>`. Fallback if Hermes renamed it (trailing slash on `/tmp/`
is required -- it's a symlink on macOS; use `-mmin`, not `-newermt "-5 minutes"`):

```bash
find /tmp/ ~/ -maxdepth 1 \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) \
  -mmin -5 2>/dev/null -exec ls -t {} + | head -1
```

Surface the same way as the direct path (step 3 above: `open <path>` to show it in
Preview, plus `SendUserFile`). Don't use `--yolo` (the auto-mode classifier blocks
it; the shell/script allowlist already lets the seedream skill run).
