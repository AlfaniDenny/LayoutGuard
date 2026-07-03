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
  - `.github/skills/create-pptx/` presentation generation skill assets
- `schematic-analyzer/`
  - `scripts/` core analyzer and CLI implementation
  - `patterns/` protocol and rule pattern definitions
  - `tests/` automated test coverage
- `LICENSE`

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

- `__pycache__/` and other generated artifacts may appear after local execution.
- Presentation automation assets are available under:
  - `BTS7xxx-1EPP/.github/skills/create-pptx/`
- Keep commits focused (small, reviewable changes).

## Maintainer

- Alfani Denny
