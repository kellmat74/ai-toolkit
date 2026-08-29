# FLUX.2 Pro Details

FLUX.2 Pro is a 32-billion parameter multimodal image generation and editing model by Black Forest Labs. It uses a latent flow matching architecture combining a Mistral-3 24B vision-language model with a rectified flow transformer, enabling direct text-to-image mapping for high prompt adherence and visual quality.

Key features:
- Free on OpenRouter (input $0/1M tokens, output $0/1M tokens)
- ~46K token context window
- Excels at prompt adherence and visual quality
- Supports text-image inputs (editing) but for pure generation use `modalities: ["image"]`
- High-resolution outputs (up to 4K)
- Strong performance on complex prompts and detailed scenes

References:
- OpenRouter model page: https://openrouter.ai/black-forest-labs/flux.2-pro
- Black Forest Labs blog: https://blackforestlabs.ai/flux-2-pro
