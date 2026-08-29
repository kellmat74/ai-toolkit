# Using ImageMagick for Pixel Art Generation

ImageMagick can be used to create simple pixel art without relying on Python/Pillow.

## Basic Pixel Art Anvil (32x32)

```bash
magick -size 32x32 xc:#FFA500 -fill black \
  -draw "rectangle 6,28 26,32" \
  -draw "polygon 10,16 22,16 26,28 6,28" \
  -draw "rectangle 22,8 26,16" \
  /tmp/anvil_pixel.png
```

## Explanation

- `-size 32x32 xc:#FFA500`: Create a 32x32 orange background
- `-fill black`: Set drawing color to black
- `-draw "rectangle 6,28 26,32"`: Draw the base of the anvil
- `-draw "polygon 10,16 22,16 26,28 6,28"`: Draw the body (trapezoid)
- `-draw "rectangle 22,8 26,16"`: Draw the horn on the right

## Scaling Up for Visibility

To view the pixel art at a larger size without blurring:

```bash
magick /tmp/anvil_pixel.png -scale 128x128 /tmp/anvil_pixel_128.png
```

The `-scale` filter uses nearest-neighbor interpolation by default, preserving the hard pixel edges.

## Advantages

- No Python dependencies required
- Fast and available on most systems via `imagemagick` package
- Good for simple shapes and logos

## Limitations

- More complex dithering and color quantization (like Floyd-Steinberg) is harder to achieve
- For advanced pixel art with palettes and dithering, the Python/Pillow approach in `scripts/pixel_art.py` is recommended.

## Installation

On macOS with Homebrew:
```bash
brew install imagemagick
```