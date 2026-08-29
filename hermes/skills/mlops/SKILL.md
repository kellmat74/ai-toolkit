---
name: mlops
description: "Umbrella skill for machine learning operations tools and workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mlops, machine-learning, operations]
    related_skills: [audiocraft-audio-generation, dspy, evaluating-llms-harness, huggingface-hub, llama-cpp, obliteratus, openrouter-image-generation, segment-anything-model, serving-llms-vllm, weights-and-biases]
---

# MLOps Skills Umbrella

This skill serves as an umbrella for various machine learning operations (MLOps) tools and workflows, including model serving, inference, training, evaluation, and data management.

## Subskills

The following subskills are covered under this umbrella:

- audiocraft-audio-generation: Audio generation using AudioCraft (MusicGen, AudioGen). (see `references/audiocraft-audio-generation/` for detailed documentation)
- dspy: DSPy: declarative LM programs, auto-optimize prompts, RAG. (see `references/dspy.md`)
- evaluating-llms-harness: LM-Eval-Harness: benchmark LLMs (MMLU, GSM8K, etc.). (see `references/evaluating-llms-harness.md`)
- huggingface-hub: HuggingFace hf CLI: search/download/upload models, datasets. (see `references/huggingface-hub.md`)
- llama-cpp: llama.cpp local GGUF inference + HF Hub model discovery. (see `references/llama-cpp.md`)
- obliteratus: OBLITERATUS: abliterate LLM refusals (diff-in-means). (see `references/obliteratus.md`)
- openrouter-image-generation: Generate images using models hosted on OpenRouter. (see `references/openrouter-image-generation.md`)
- segment-anything-model: SAM: zero-shot image segmentation via points, boxes, masks. (see `references/segment-anything-model.md`)
- serving-llms-vllm: vLLM: high-throughput LLM serving, OpenAI API, quantization. (see `references/serving-llms-vllm.md`)
- weights-and-biases: W&B: log ML experiments, sweeps, model registry, dashboards. (see `references/weights-and-biases.md`)
- image-processing: Image processing: generation and segmentation using models like SAM and OpenRouter-hosted models. (see `references/image-processing/` for detailed documentation)
- llm-ops: LLM Operations: evaluation, serving, and model hub management. (see `references/llm-ops/` for detailed documentation)

Each subskill has its own detailed documentation in the `references/` directory. For example, see `references/audiocraft-audio-generation/` for the audiocraft-audio-generation subskill.

## Usage

When working with MLOps tasks, load this skill to access the relevant subskills. The umbrella skill provides guidance on choosing the right subskill for your MLOps workflow.