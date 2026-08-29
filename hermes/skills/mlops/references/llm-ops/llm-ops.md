---
name: llm-ops
description: "LLM Operations: evaluation, serving, and model hub management."
version: 1.0.0
author: Hermes Curator
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [LLM, Operations, Evaluation, Serving, Hub]

---
# LLM Operations (LLM-Ops)

This skill covers the end-to-end operations of Large Language Models (LLMs), including evaluation, serving, and model hub interactions.

## Overview

LLM-Ops encompasses the practices and tools for deploying, evaluating, and managing LLMs in production and development environments.

## Sections

### LLM Evaluation
See [evaluating-llms-harness] for benchmarking LLMs using the lm-evaluation-harness.

### LLM Serving
See [serving-llms-vllm] for high-throughput LLM serving with vLLM.

### Model Hub Management
See [huggingface-hub] for managing models, datasets, and Spaces on the Hugging Face Hub.

## Workflows

### Typical LLM Deployment Pipeline
1. **Select a model** from a model hub (e.g., Hugging Face Hub).
2. **Evaluate the model** on relevant benchmarks to assess quality.
3. **Serve the model** using an optimized inference server (e.g., vLLM) for deployment.
4. **Monitor and iterate** based on performance and feedback.

## References
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [vLLM](https://github.com/vllm-project/vllm)
- [Hugging Face Hub](https://huggingface.co)

---