# LayoutGuard — AI-Powered Schematic Design Review

Automated hardware design review for Infineon BTS7xxx
High-Side Switch family using GitHub Copilot and the
LayoutGuard integrated Schematic Analyzer CLI tool.

---

## What This Does

Reviews KiCad schematic files (.kicad_sch) against
Infineon official hardware design guidelines for the
BTS7xxx Smart7 family — automatically, pin by pin.

Replaces manual cross-checking between Excel design
checklist and schematic. Produces consistent,
evidence-based review reports every time.

---

## Supported Variants

| Type           | Package | Variants                          |
|----------------|---------|-----------------------------------|
| Single Channel | 1EPP    | BTS7002/04/06/08/10 -1EPP         |
| Single Channel | 1EPA    | BTS7002/04 -1EPA                  |
| Single Channel | 1EPZ    | BTS7002/04 -1EPZ                  |
| Dual Channel   | 2EPP    | BTS7002/04 -2EPP                  |
| Dual Channel   | 2EPA    | BTS7002/04 -2EPA                  |
| Dual Channel   | 2EPZ    | BTS7002/04 -2EPZ                  |

To add a new variant: update `DEVICE VARIANT CONFIGURATION`
section in the guidance file only. All rules apply automatically.

---

## Prerequisites

Install all of the following before use:

| Tool                | Version    | Download                          |
|---------------------|------------|-----------------------------------|
| Python              | 3.10+      | python.org/downloads              |
| KiCad               | 8.0+       | kicad.org/download/windows        |
| Git                 | any        | git-scm.com                       |
| VSCode              | any        | code.visualstudio.com             |
| VSCode: Python ext  | latest     | VSCode Extensions marketplace     |
| VSCode: Copilot ext | latest     | VSCode Extensions marketplace     |
| GitHub Copilot      | active sub | github.com/features/copilot       |

---

## Installation

```powershell
# 1. Clone the LayoutGuard repo
git clone https://github.com/AlfaniDenny/LayoutGuard.git
cd LayoutGuard

# 2. Install Python dependencies
pip install -r scripts\requirements.txt

# 3. Add KiCad CLI to PATH (run as Administrator)
[System.Environment]::SetEnvironmentVariable(
  "PATH",
  $env:PATH + ";C:\Program Files\KiCad\8.0\bin",
  "Machine"
)

# 4. Verify installation
python schematic-analyzer\scripts\schematic-cli.py --help
kicad-cli --version
```

---

## Project Structure

```
C:\LayoutGuard\
├── guidance\
│   └── BTS7xx_review_context.md   ← AI guidance file (all rules)
├── datasheets\
│   └── BTS7002-1EPP_DS.pdf        ← optional reference
└── schematic\
    └── your_design.kicad_sch      ← KiCad schematic to review

C:\LayoutGuard\schematic-analyzer\
└── scripts\
   └── schematic-cli.py           ← CLI tool (used by AI)
```

---

## Guidance File Structure

`BTS7xx_review_context.md` contains these sections in order:

```
1. INSTRUCTIONS FOR AI
   8-step mandatory query sequence for Copilot

2. DEVICE VARIANT CONFIGURATION       ← edit this per project
   Active variant, PIN MAP, supported variants table

3. NET DISCOVERY PROTOCOL
   How AI discovers actual net names from schematic

4. REVIEW OUTPUT FORMAT
   Standardized output format per pin

5. SCORING CRITERIA
   Definition of ✅ ❌ ⚠️ 📐 statuses

6. COMPONENT NAMING CONVENTION
   Maps functional names (RIN, RGND) to expected values
   Dual channel additional components table

7. COMMON FAULT DETECTION RULES F1–F11
   F1  Floating pin
   F2  Component missing
   F3  Isolated net
   F4  Unused pin not terminated
   F5  Optional placeholder missing
   F6  OUT pins on different nets
   F7  Value outside ±10% tolerance
   F8  Mandatory component marked DNP
   F9  Incomplete IS sensing circuit
   F10 Same cap value on VS and OUT
   F11 n.c. pin not soldered to PCB

8. PIN CHECKLIST EP + Pin 1–14
   Per-pin mandatory and optional components
   Further Info and Layout Requirements per pin
   Dual channel additional pins (IN1, DSEL, OUT_CH2)

9. QUICK REFERENCE SUMMARY TABLE
   All pins at a glance
```

## Scoring Criteria

| Status      | Symbol | Meaning                                    |
|-------------|--------|--------------------------------------------|
| PASS        | ✅     | Correct — no action needed                 |
| CRITICAL    | ❌     | Must fix before PCB manufacturing          |
| WARNING     | ⚠️     | Recommended to resolve — risk if ignored   |
| LAYOUT NOTE | 📐     | PCB layout item — requires separate review |

---

## Component Naming Convention

Three formats supported in schematic Value field:

| Format           | Example    | Value Confirmed | Recommended |
|------------------|------------|-----------------|-------------|
| Value only       | `4k7`      | ✅ Auto         |             |
| Name + Value     | `RIN_4k7`  | ✅ Auto         | ✅ YES      |
| Name only        | `RIN`      | ⚠️ BOM check   |             |

**Recommended standard:** `[FUNCTION]_[VALUE]`

```
RGND_47R    RDEN_4k7    RADC_4k7    RISPROT_4k7
RIN_4k7     RDSEL_4k7   RSENSE_1k2  ROL_10k
RIN1_4k7    CVS_100n    COUT_10n    RPD_220k
CVSGND_47n  CSENSE_220p DZ1_7V
```

---

## Fault Detection — 11 Rules

| Rule | Fault                            | Status      |
|------|----------------------------------|-------------|
| F1   | Floating pin / no wire           | ❌ CRITICAL |
| F2   | Component completely missing     | ❌ CRITICAL |
| F3   | Isolated net (pin_count = 1)     | ❌ CRITICAL |
| F4   | Unused digital pin not terminated| ⚠️ WARNING  |
| F5   | Optional placeholder missing     | ⚠️ WARNING  |
| F6   | OUT pins on different nets       | ❌ CRITICAL |
| F7   | Value outside ±10% tolerance     | ❌ CRITICAL |
| F8   | Mandatory component marked DNP   | ❌ CRITICAL |
| F9   | Incomplete IS sensing circuit    | ❌ CRITICAL |
| F10  | Same cap value on VS and OUT     | ⚠️ WARNING  |
| F11  | n.c. pin not soldered to PCB     | ⚠️ WARNING  |

---

## How to Run a Review

### Step 1 — Fill DEVICE VARIANT CONFIGURATION
Open `BTS7xx_review_context.md` and update:
```
DEVICE_REF        : U1
DEVICE_PART       : BTS7002-1EPP
PACKAGE           : 1EPP
CHANNEL_COUNT     : 1
PIN MAP           : update pin numbers from datasheet
```

### Step 2 — Open VSCode Workspace
```
File → Add Folder to Workspace
   Add: C:\LayoutGuard\BTS7xxx-1EPP\
   Add: C:\LayoutGuard\schematic-analyzer\
```

### Step 3 — Open Copilot Chat
```
Ctrl + Shift + I
```

### Step 4 — Paste Review Prompt
```
I will be reviewing a KiCad schematic for a BTS7xx family
IC (Infineon High-Side Switch).

Use this guidance file as the sole reference:
@BTS7xx_review_context.md

Schematic:
C:\LayoutGuard\BTS7xxx-1EPP\schematic\your_design.kicad_sch

CLI tool:
C:\LayoutGuard\schematic-analyzer\scripts\schematic-cli.py

Read DEVICE VARIANT CONFIGURATION first.
Follow the 8-step MANDATORY SEQUENCE in INSTRUCTIONS FOR AI.
Skip pins marked "-" in PIN MAP.
Produce full report per pin + summary table at the end.
```

---

## Review Output Format

```
### [Pin Number] — [Pin Name]
Component Found : [ref] = [value]
Status          : ✅ PASS / ❌ CRITICAL / ⚠️ WARNING / 📐 NOTE
Detail          : [explanation]
Recommendation  : [action required if not PASS]
```

**Summary table at end of report:**
```
| Pin  | Component  | Status      |
|------|------------|-------------|
| EP   | C3=100nF   | ✅ PASS     |
| 1    | R2=47Ω     | ✅ PASS     |
| 2    | R5=RIN_4k7 | ✅ PASS     |
| ...  | ...        | ...         |
```

---

## Scope and Limitations

**In scope (automated):**
- Component presence and value verification
- Net connectivity verification
- All 11 fault rules F1–F11
- Single and dual channel variants
- All EPP / EPA / EPZ packages

**Out of scope (manual review needed):**
- PCB layout verification (.kicad_pcb)
- BOM vs schematic value discrepancy
- Via count and PCB area connection style
- Component placement distance to IC pin

---

## Files Required

| File                         | Purpose                    |
|------------------------------|----------------------------|
| `BTS7xx_review_context.md`   | AI guidance — all rules    |
| `your_design.kicad_sch`      | KiCad schematic to review  |
| `schematic-cli.py`           | CLI tool from LayoutGuard repo |

---

## Author / Maintainer

Guidance source : Infineon BTS7xxx Application Note
Tool source     : github.com/AlfaniDenny/LayoutGuard
Review system   : GitHub Copilot + VSCode
Maintainer      : Alfani Denny

## Copyright and Attribution

- For code/content derived from the original upstream source, existing copyright attribution to Seeed Studio is intentionally preserved.
- New contributions in this repository may include additional copyright attribution to Alfani Denny.
- Attribution for new contributions is additive and does not replace upstream attribution.