---
name: security-audit
description: Deep security assessment of a feature, service, or codebase: parallel vulnerability, attack-surface, and compliance passes merged into a severity-ranked report with a remediation plan. Use for a full audit before launch or on request; for a quick security pass on a diff or PR, use review-code instead.
---

# Security Audit

## Trigger
`/security-audit <code, feature, or requirement>`

This is the DEEP assessment. The `review-code` skill already does a lighter security
pass on a diff; use this one when the ask is a real audit: a whole feature, service,
auth system, or codebase, assessed for vulnerabilities, attack surface, and compliance.

## Workflow

### 1. Scope the audit
Identify what is under audit and pick the audit type:
- New feature implementation
- API endpoints and data flows
- Authentication/authorization system
- Infrastructure configuration
- Dependency security (CVE scan)
- Compliance verification

Enumerate the concrete surface: repos/paths, endpoints, data stores, secrets locations,
third-party integrations. Note what handles sensitive data.

### 2. Delegate parallel read-only passes
Spawn all three via the Task tool in parallel, each with the same scope, each read-only.
Keep the passes independent; they should not see each other's findings before reporting.

**`security-auditor`: code vulnerabilities**
1. Authentication & authorization: credential handling, token management, session
   security, permission checks, MFA
2. Input validation: SQL injection, XSS, command injection, path traversal,
   deserialization of untrusted data
3. Data protection: encryption at rest, TLS in transit, sensitive data handling, PII
   protection, retention policies
4. Secret management: hardcoded credentials, env var security, rotation, access
   control, audit logging
5. Dependency security: known CVEs, version constraints, transitive dependencies,
   supply chain

Each finding uses this template:
```
Vulnerability: [Name]
Severity: [Critical/High/Medium/Low]
Type: [Category]
Location: [File:Line or Component]
Description / Impact / Reproduction / Remediation
CWE: [ID]   CVSS: [if applicable]
```

**`penetration-tester`: attack surface and methodology**
1. Attack surface mapping: entry points, all endpoints, hidden/forgotten services,
   data flows
2. Exploit analysis (methodology and evidence from the code, no live exploitation
   without explicit user sign-off): SQL injection vectors, XSS payload paths, auth
   bypass, authz bypass, business logic attacks
3. Resilience: DoS exposure, rate limiting effectiveness, resource exhaustion,
   connection limits

**`compliance-specialist`: regulatory and standards**
1. Data protection regulations: GDPR, CCPA, HIPAA, PCI-DSS as applicable. HIPAA
   awareness matters here (healthcare RCM domain), but note the org policy is never to
   process PHI, so the check is "does this system correctly avoid ingesting/storing
   PHI" as much as "does it handle it compliantly".
2. Security standards: OWASP Top 10, NIST CSF, ISO 27001, CIS Benchmarks
3. Internal policies: data handling procedures, access control, audit logging
   requirements

**`security-engineer`: infrastructure security (optional fourth pass)**
Add this pass when the audit scope includes infrastructure, deployment, or cloud
config (IaC, CI/CD, secrets management, network policy), not just application code.
1. Secrets management: how credentials are stored, rotated, injected
2. Infrastructure hardening: network exposure, TLS config, IAM/least privilege
3. CI/CD pipeline security: supply chain, artifact integrity, deploy credentials

### 3. Merge findings
1. Collect all reports
2. Consolidate and deduplicate (keep the more specific finding, note when multiple
   passes caught it)
3. Prioritize by severity, calculate risk scores

| Severity | Likelihood | Impact | CVSS | Action |
|----------|-----------|--------|------|--------|
| Critical | High | Severe | 9.0-10.0 | Fix immediately, block deployment |
| High | High/Medium | Major | 7.0-8.9 | Fix before release, escalate |
| Medium | Medium/Low | Moderate | 4.0-6.9 | Fix in next iteration |
| Low | Low | Minor | 0.1-3.9 | Backlog, fix if time |

### 4. Report

```
SECURITY AUDIT REPORT
=====================
Subject / Date / Overall risk level / Status: Pass | Conditional | Fail

EXECUTIVE SUMMARY
Findings: Critical [n], High [n], Medium [n], Low [n]
Critical findings listed, recommendation stated.

FINDINGS BY SEVERITY
[Each finding per the template above, Critical first]

COMPLIANCE STATUS
GDPR / CCPA / HIPAA (or N/A with PHI-avoidance verified) / PCI-DSS / OWASP Top 10
Non-compliant areas listed.

ATTACK SURFACE SUMMARY
Entry points, tested vectors, and results.

REMEDIATION PLAN
Critical: fix immediately, with owner and date
High: fix within 1 week
Medium: fix within 1 month
Low: backlog
```

## Vulnerability categories (reference)
- CWE-79: Cross-site Scripting (XSS)
- CWE-89: SQL Injection
- CWE-798: Hardcoded Credentials
- CWE-863: Incorrect Authorization
- CWE-22: Path Traversal
- CWE-352: Cross-Site Request Forgery (CSRF)
- CWE-434: Unrestricted File Upload
- CWE-502: Deserialization of Untrusted Data

## Principles
1. Secure by design, not afterthought
2. Defense in depth
3. Fail closed, not open
4. Least privilege
5. Assume breach
6. Never trust user input; always encode output
7. Never hardcode credentials
8. Audit trails for everything
9. Keep dependencies current

## Persistence
This audit changes nothing; findings are for the user to act on. If it surfaces
something durable (a recurring vulnerability class in this codebase, a compliance
posture decision), propose saving it to the Obsidian vault via the vault skill. Ask
before writing.
