---
name: generate-image
description: Generate an image from this Claude Code surface by routing the prompt through the local Hermes agent's seedream skill (Seedream 4.5 via OpenRouter), then surfacing the result inline. Use when the user asks to generate, create, draw, or make an image, picture, illustration, or logo.
---

# Generate an image (via Hermes + Seedream 4.5)

Claude Code has no native image generation. This skill routes the request to the
local Hermes agent, which runs the `seedream` skill (Seedream 4.5 over OpenRouter),
then shows the result here. See `driving-hermes` for the Hermes CLI mechanics this
builds on, and `hermes/skills/seedream.md` for the underlying API recipe.

**Cost:** $0.04 per image (Seedream 4.5, fixed). Each run bills once. If a run
reports no image, it may still have billed -- read the output before retrying.

## Steps

1. **Get a clean prompt.** Use the user's description verbatim as the image prompt.
   If it's a one-word request ("a logo"), ask one quick clarifying question rather
   than guessing. Don't pad the prompt with your own embellishments unless asked.

2. **Drive Hermes**, telling it exactly where to save and how to report the path so
   the output is parseable (Hermes otherwise picks its own filename). Run it as a
   **background task** -- a full agent run takes a few minutes and `--cli` only
   flushes output on completion (see `driving-hermes`):

   ```bash
   REPO=~/git/personal/ai-toolkit
   OUT=/tmp/claude_genimg_$(date +%s).jpg
   hermes --cli --skills "$REPO/hermes/skills" -z "Use the seedream skill to \
   generate an image. Prompt: <PROMPT>. Save the result to exactly $OUT and then \
   print one final line: SAVED:$OUT . Do not rename the file." 2>&1 \
     | tee /tmp/hermes_genimg.log
   ```

   Substitute `<PROMPT>` and keep the `$OUT` path consistent in both the prompt and
   the marker so you can grep for it.

3. **Locate the file.** Parse `SAVED:<path>` from the output. If Hermes deviated and
   named it something else (it sometimes does), fall back to finding the newest
   image written in the last few minutes:

   ```bash
   # Trailing slash on /tmp/ is REQUIRED on macOS: /tmp is a symlink to
   # /private/tmp and `find /tmp -maxdepth 1` won't descend into it.
   # -mmin -5 = modified in last 5 min (use this, not -newermt "-5 minutes",
   # which silently matches nothing on BSD/macOS find).
   find /tmp/ ~/ -maxdepth 1 \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) \
     -mmin -5 2>/dev/null -exec ls -t {} +  | head -1
   ```

4. **Verify it's real**, not a zero-byte stub or an error JSON saved as `.jpg`:

   ```bash
   file <path>   # expect "JPEG image data" or "PNG image data" with dimensions
   ```

5. **Surface it** to the user with `SendUserFile` (status `normal`), caption with the
   prompt used. Then state the cost ($0.04) and the saved path. Remind the user that
   `/tmp` is cleared on reboot if they want to keep it.

## Notes

- This is the slow-but-hands-off path (full Hermes agent spin-up, minutes). It's the
  design the user asked for: Claude Code as the front door, Hermes as the executor.
- If you ever need an image FAST and just for yourself (not exercising the Hermes
  path), the same API can be called directly per `hermes/skills/seedream.md` -- but
  default to routing through Hermes so behavior matches what runs async/scheduled.
- Don't use `--yolo` (the auto-mode classifier blocks it). The shell/script
  allowlist lets the seedream skill run without per-step approval.
