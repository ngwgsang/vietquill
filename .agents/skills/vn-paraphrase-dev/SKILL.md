---
name: vn-paraphrase-dev
description: Workflow for developing Vietnamese paraphrase generation components. Use this skill when implementing new metrics, estimators, or models to ensure consistency and automated script generation.
---

# Vietnamese Paraphrase Generation Development

This skill guides the development of components for the Quality-Controlled Paraphrase Generation for Vietnamese project.

## Workflow

### 1. Component Implementation
- **Metrics**: Implement in `src/utils/metrics/`. Inherit from `BaseMetric`.
- **Estimators**: Implement in `src/utils/estimators/`. Inherit from `BaseEst`.
- **Models/Inference**: Implement in `src/finetune/` or `src/inference/`.

### 2. Script Generation
After implementing a new component, you MUST create a shell script (`.sh`) in the corresponding subdirectory of `scripts/`.

Use the standard template:
```bash
#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH to include the current directory (project root)
export PYTHONPATH=$PYTHONPATH:.

# Run [Component Name] using the virtual environment's python
./venv/Scripts/python.exe [Path to python file] \
    [Default arguments]
```

#### Directory Mapping for Scripts:
- `src/utils/metrics/*.py` -> `scripts/metrics/run_*.sh`
- `src/utils/estimators/*.py` -> `scripts/est/run_*.sh`
- `src/finetune/*.py` -> `scripts/finetune/run_*.sh`

### 3. Verification & Reporting
- You do NOT need to run the `.sh` script after creation.
- Simply report the name and path of the generated script to the user.
- Ensure the script follows the template correctly and all paths are accurate.

## Standards
- Always use `python.exe` from the `./venv/Scripts/` directory for Windows compatibility in scripts.
- Ensure all scripts set `PYTHONPATH` to the project root.
- All metrics and estimators should have a CLI interface (using `argparse`).
