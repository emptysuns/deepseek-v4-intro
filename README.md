---
title: DeepSeek V4 Pro introdutions
emoji: 🐋
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 8080
pinned: false
license: mit
---

# DeepSeek-V4-Pro Interactive Showcase

> **Towards Highly Efficient Million-Token Context Intelligence**

An interactive demo showcasing **DeepSeek-V4-Pro**, DeepSeek-AI's latest Mixture-of-Experts large language model with 1 million token context support. Explore its capabilities across reasoning, coding, mathematics, and long-context tasks.

---

## Model Overview

| Specification | Value |
|:---|:---|
| **Architecture** | Mixture-of-Experts (MoE) |
| **Total Parameters** | 1.6 Trillion (1.6T) |
| **Activated Parameters** | 49B |
| **Context Length** | 1,000,000 tokens |
| **Training Data** | 32T+ tokens |
| **Precision** | FP4 + FP8 Mixed |
| **License** | MIT |

---

## Architecture Innovations

### Hybrid Attention: CSA + HCA
Combines **Compressed Sparse Attention (CSA)** with **Heavily Compressed Attention (HCA)**. At 1M-token context, requires only **27% of single-token inference FLOPs** and **10% of KV cache** compared to DeepSeek-V3.2.

### Manifold-Constrained Hyper-Connections (mHC)
Strengthens residual connections to enhance stability of signal propagation across layers while preserving model expressivity.

### Muon Optimizer
Enables faster convergence and greater training stability during the 32T+ token pre-training phase.

---

## Reasoning Modes

| Mode | Description | Context Requirement |
|:---|:---|:---|
| **Non-think** | Fast, intuitive responses | Default |
| **Think High** | Conscious logical analysis with visible reasoning | Default |
| **Think Max** | Maximum reasoning effort for complex problems | 384K+ context |

---

## Benchmark Highlights

### Coding and Reasoning

| Benchmark | V4-Pro Max Score | Notes |
|:---|:---|:---|
| **LiveCodeBench** | **93.5** | Best among frontier models |
| **Codeforces** | **3206** | Best among frontier models |
| **Apex Shortlist** | **90.2** | Best among frontier models |
| SWE Verified | 80.6 | Near Opus 4.6 (80.8) |

### Mathematics

| Benchmark | V4-Pro Max Score | Notes |
|:---|:---|:---|
| **IMOAnswerBench** | 89.8 | Close to GPT-5.4 (91.4) |
| GSM8K (8-shot, Base) | 92.6 | — |
| MATH (4-shot, Base) | 64.5 | — |

### Knowledge and General

| Benchmark | V4-Pro Max Score | Notes |
|:---|:---|:---|
| MMLU-Pro | 87.5 | — |
| GPQA Diamond | 90.1 | — |
| BrowseComp | 83.4 | — |
| HLE (Pass@1) | 37.7 | — |

### Long Context

| Benchmark | V4-Pro Max Score | Notes |
|:---|:---|:---|
| MRCR 1M | 83.5 | 1M token evaluation |
| LongBench-V2 (Base) | 51.5 | — |

---

## Companion Model: DeepSeek-V4-Flash

| Specification | V4-Flash |
|:---|:---|
| **Total Parameters** | 284B |
| **Activated Parameters** | 13B |
| **Context Length** | 1,000,000 tokens |
| **Performance** | Comparable reasoning to Pro with larger thinking budget |

---

## Deployment

**Supported Libraries**: Transformers / vLLM / SGLang / Docker Model Runner

**Recommended Sampling** (Think Max): `temperature = 1.0, top_p = 1.0`

**Community**: 16 quantized versions / 9 finetunes / 100+ HF Spaces / 3M+ downloads/month

---

## License

Released under the **MIT License** by DeepSeek-AI (2026).

---

*This Space provides an interactive interface to explore DeepSeek-V4-Pro's capabilities. Try it out with coding challenges, math problems, or long-document analysis.*
