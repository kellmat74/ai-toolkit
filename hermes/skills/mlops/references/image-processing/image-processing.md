---
name: image-processing
description: "Image processing: generation and segmentation using models like SAM and OpenRouter-hosted models."
version: 1.0.0
author: Hermes Curator
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Image, Processing, Generation, Segmentation, SAM, OpenRouter]

---
# Image Processing

This skill covers image processing tasks including image generation and segmentation.

## Overview

Image processing encompasses techniques for generating images from text and segmenting images into meaningful regions.

## Sections

### Image Generation
See [openrouter-image-generation] for generating images using models hosted on OpenRouter (e.g., Seedream, Flux).

### Image Segmentation
See [segment-anything-model] for zero-shot image segmentation using the Segment Anything Model (SAM).

## Workflows

### Typical Image Generation Workflow
1. **Select a model** from an image generation model hub (e.g., OpenRouter).
2. **Prepare a prompt** describing the desired image.
3. **Generate the image** using the model via API.
4. **Post-process** the image if needed (e.g., resizing, format conversion).

### Typical Image Segmentation Workflow
1. **Select a segmentation model** (e.g., SAM ViT-H, ViT-L, ViT-B).
2. **Prepare the image** and optional prompts (points, boxes, or masks).
3. **Generate masks** using the model with the provided prompts.
4. **Refine masks** iteratively if needed using additional prompts.

## References
- [Segment Anything Model](https://github.com/facebookresearch/segment-anything)
- [OpenRouter](https://openrouter.ai)

---