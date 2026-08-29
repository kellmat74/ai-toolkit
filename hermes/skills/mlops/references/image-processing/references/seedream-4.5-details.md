# Seedream 4.5 Specifics for OpenRouter

## Model Overview
Seedream 4.5 is ByteDance's flagship image generation model, delivering industry-leading text rendering and multi-image consistency at a competitive price point.

## Key Capabilities
- **Text Rendering Industry Leader**: Unlike models like Flux 2 that struggle with typography, Seedream 4.5 renders accurate, readable text with correct spelling for complex words and phrases
- **High-Resolution Output**: Generates images up to 4K resolution (approximately 4096x4096 or equivalent aspect ratios)
- **Multi-Reference Input**: Accepts up to 10 reference images in a single generation request
- **Unified Architecture**: Uses a single API endpoint for both text-to-image and image-to-image generation
- **Multi-Image Composition**: Significantly strengthened capabilities for creating consistent visuals across multiple outputs

## Technical Specifications
- **Price**: $0.04 per output image (regardless of size)
- **Context**: 4K
- **Released**: December 23, 2025
- **Modalities**: Image generation only (use `modalities: ["image"]`)

## Ideal Use Cases
- Marketing materials and brand assets where text accuracy is critical
- Social media graphics with correctly-spelled product names and taglines
- Professional posters with multi-line headlines that are actually readable
- E-commerce product photography requiring consistent lighting and composition
- Any visual that combines imagery with text overlays

## OpenRouter API Specifics
When using Seedream 4.5 via OpenRouter:
- Model identifier: `bytedance-seed/seedream-4.5`
- Required parameter: `modalities: ["image"]`
- Response format: Images returned as base64-encoded data URLs in the `image_url.url` field
- Pricing on OpenRouter: Matches the model's list price of $0.04 per image

## Prompt Engineering Tips for Seedream 4.5
1. **Be Specific About Text**: Clearly specify what text should appear in the image and its style
   - Example: "Include the text 'Volunteers Needed' in bold, sans-serif font at the bottom"
   
2. **Leverage Text Strength**: Since text rendering is the model's strength, make text a key element of your prompt
   
3. **Reference Images**: For consistent branding, provide up to 10 reference images to guide aesthetic, color palette, and artistic style
   
4. **Style Guidance**: While Seedream 4.5 excels at realism, you can still guide the artistic style through descriptive prompts

## Example Prompts
- "Create a professional marketing poster for a coffee shop with the text 'Artisan Brew Co.' and 'Est. 2024' in elegant script font"
- "Design a book cover for a fantasy novel titled 'The Crystal Kingdom' with magical elements and the title in golden, embossed lettering"
- "Generate a social media graphic for a yoga retreat with serene colors, lotus flowers, and the text 'Find Your Inner Peace' in flowing cursive"
- "Produces a food menu for a rustic Italian restaurant with dish names and prices in readable, classic typography"

## References
- OpenRouter Model Page: https://openrouter.ai/bytedance-seed/seedream-4.5
- Seedream 4.5 Official Information: https://seed.bytedance.com/en/seedream4_5