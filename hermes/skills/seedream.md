---
name: seedream
description: Generate an image with ByteDance Seedream 4.5 via OpenRouter. Use when the user asks to generate, create, or draw an image.
version: 1.0.0
author: kellmat74
platforms: [macos]
metadata:
  hermes:
    tags: [image-generation, seedream, openrouter]
---

# Seedream 4.5 Image Generation

Generate images using ByteDance Seedream 4.5 through OpenRouter.

**Two non-obvious requirements that make this work:**

1. OpenRouter image generation uses the chat completions endpoint with
   `modalities: ["image"]`, NOT the standard `/v1/images/generations` endpoint.
   The built-in `image_gen` toolset does not work for this; use this skill.
2. The image bytes come back in `message.images[0].image_url.url` as a base64
   data URL. **Parse the raw JSON yourself.** Do NOT use the OpenAI Python SDK:
   its typed `ChatCompletionMessage` drops the non-standard `images` field, so
   `hasattr(message, "images")` is False and the image is silently lost AFTER you
   have already been billed for it. This is the bug that burned credits without
   ever saving a file.
3. TLS on this machine is intercepted (Tirith). Plain urllib/curl with default
   certs fails the handshake. You MUST verify against the Hermes CA bundle at
   `~/.hermes/certs/combined_ca_bundle.pem`.

## Steps

1. Extract the image prompt from the user's request.

2. Write and run this Python script, substituting the prompt:

```python
import json, base64, os, sys, ssl, time, urllib.request

PROMPT = "<user prompt here>"

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
if not API_KEY:
    _env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(_env_file):
        with open(_env_file) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line.startswith("OPENROUTER_API_KEY=") and not _line.startswith("#"):
                    API_KEY = _line.split("=", 1)[1].strip()
                    break
if not API_KEY:
    print("Error: OPENROUTER_API_KEY not found in env or ~/.hermes/.env")
    sys.exit(1)

# TLS is intercepted on this machine; verify against the Hermes CA bundle.
_bundle = os.path.expanduser("~/.hermes/certs/combined_ca_bundle.pem")
ctx = ssl.create_default_context(cafile=_bundle) if os.path.exists(_bundle) \
    else ssl.create_default_context()

payload = json.dumps({
    "model": "bytedance-seed/seedream-4.5",
    "messages": [{"role": "user", "content": PROMPT}],
    "modalities": ["image"]
}).encode()

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=payload,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://hermes-agent.nousresearch.com",
        "X-Title": "Hermes Agent",
    }
)
with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
    data = json.loads(resp.read())

msg = data["choices"][0]["message"]
image_url = None
if "images" in msg and msg["images"]:
    image_url = msg["images"][0]["image_url"]["url"]
elif isinstance(msg.get("content"), list):
    for block in msg["content"]:
        if block.get("type") == "image_url":
            image_url = block["image_url"]["url"]
            break

if not image_url:
    print("No image in response (you may still have been billed):")
    print(json.dumps(data, indent=2)[:1500])
    sys.exit(1)

# data URL looks like: data:image/jpeg;base64,<...>  -- keep the real extension
ext = "jpg"
if image_url.startswith("data:image/"):
    ext = image_url.split("/", 1)[1].split(";", 1)[0]
outfile = f"/tmp/seedream_{int(time.time())}.{ext}"
if image_url.startswith("data:"):
    b64 = image_url.split(",", 1)[1]
    with open(outfile, "wb") as f:
        f.write(base64.b64decode(b64))
else:
    urllib.request.urlretrieve(image_url, outfile)

cost = data.get("usage", {}).get("cost")
print(f"saved:{outfile}  cost:${cost}")
```

3. Parse `saved:<path>` from the output and tell the user the image path. Open
   the file with `open <path>` so it displays in Preview, or use the vision tool
   to describe it back if the user wants a preview in chat.

## Error handling

- `OPENROUTER_API_KEY not found` -- key missing from both env and `~/.hermes/.env`.
- TLS handshake failure / empty response -- the CA bundle path is wrong or missing.
- HTTP 402 -- insufficient OpenRouter credits.
- `No image in response` -- you were likely still billed $0.04. Print the raw JSON
  to see what came back before retrying, so you don't burn more credits blindly.

## Cost

$0.04 per image (OpenRouter pricing for Seedream 4.5). This is fixed regardless
of image size or resolution.
