# LayoutGuard

LayoutGuard is a unified workspace repository for schematic review and rule-based analysis.

This repository combines:
- `BTS7xxx-1EPP`: project review inputs/outputs, schematics, and guidance assets
- `schematic-analyzer`: Python-based schematic analysis tooling, patterns, and tests

## Repository Structure

- `BTS7xxx-1EPP/`
  - KiCad project files
  - Datasheet and review context artifacts
  - `review_cli/` generated review outputs
- `schematic-analyzer/`
  - `scripts/` core analyzer and CLI implementation
  - `patterns/` protocol and rule pattern definitions
  - `tests/` automated test coverage
- `LICENSE`
- `README.md`
- `.gitignore`

## Quick Start

### 1. Clone

```bash
git clone https://github.com/AlfaniDenny/LayoutGuard.git
cd LayoutGuard
```

### 2. Python environment (recommended)

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

### 3. Install analyzer dependencies

```bash
pip install -r schematic-analyzer/scripts/requirements.txt
```

### 4. Run tests

```bash
pytest schematic-analyzer/tests
```

### 5. Optional: run analyzer CLI

```bash
python schematic-analyzer/scripts/schematic-cli.py --help
```

## Working Workflow

Typical daily workflow:

```bash
git pull
git status
git add .
git commit -m "your message"
git push
```

Current default branch: `main`

## Notes

- Generated local artifacts such as `__pycache__/` are ignored via `.gitignore`.
- The local BTS `.github` skill folder is intentionally excluded from this repository.
- Keep commits focused (small, reviewable changes).

## Maintainer

- Alfani Denny
