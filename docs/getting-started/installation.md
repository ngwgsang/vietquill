# Installation

This guide walks you through setting up VietQuill in your Python environment.

## Prerequisites

- **Python**: `>= 3.10`
- **PyTorch**: `>= 2.0.0` (with CUDA support recommended for GPU acceleration)

## Basic Installation

You can install VietQuill directly from PyPI using `pip`:

```bash
pip install vietquill
```

Or install in editable mode from source:

```bash
git clone https://github.com/ngwgsang/vietquill.git
cd vietquill
pip install -e .
```

## Installing Optional Documentation Dependencies

If you wish to build or preview this documentation locally:

```bash
pip install "vietquill[docs]"
```

Or manually:

```bash
pip install mkdocs-material mkdocstrings[python] mkdocs-autorefs
```

## GPU Acceleration Setup (PyTorch with CUDA)

VietQuill models use Seq2Seq transformers (such as ViT5) and neural estimators (vELECTRA). A CUDA-enabled GPU significantly speeds up inference.

If you have an NVIDIA GPU, install the appropriate PyTorch build according to your CUDA driver:

```bash
# Example for CUDA 12.1
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

Verify your GPU is available:

```python
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Device Name: {torch.cuda.get_device_name(0)}")
```

VietQuill automatically selects `cuda` if available, and falls back to `cpu` otherwise.
