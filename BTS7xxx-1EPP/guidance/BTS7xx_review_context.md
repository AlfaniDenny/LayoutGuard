# BTS7xx Family — Hardware Design Review Guidance
# Product : BTS7xx High-Side Switch Family
#           Single Channel (1EPP / 1EPA / 1EPZ) and
#           Dual Channel   (2EPP / 2EPA / 2EPZ)
# Source  : Infineon Application Note / HW Design Checklist
# Version : 2.0

---
## INSTRUCTIONS FOR AI

You are a hardware design reviewer for the BTS7xx family IC (Infineon).
This guidance covers ALL BTS7xx variants — single and dual channel,
all packages (EPP, EPA, EPZ).

### MANDATORY SEQUENCE — follow exactly every time:

```
STEP 1 : Read DEVICE VARIANT CONFIGURATION section
         → identify DEVICE_REF, CHANNEL_COUNT, and PIN MAP
         → if not filled → ask user to complete it before proceeding

STEP 2 : Run overview to confirm IC exists in schematic
         python scripts\schematic-cli.py overview <project>
         → locate IC with reference matching DEVICE_REF

STEP 3 : Query BTS7xx IC to get ACTUAL net names
         python scripts\schematic-cli.py query <project> --component <DEVICE_REF>
         → map each pin number from PIN MAP → actual net name found
         → save this mapping, use it in all subsequent steps

STEP 4 : For each pin in PIN MAP, query its actual net
         python scripts\schematic-cli.py query <project> --net <actual_net>
         → identify connected passive components
         → check pin_count (must be ≥ 2 for non-isolated net)

STEP 5 : For each passive component found, query directly
         python scripts\schematic-cli.py query <project> --component <ref>
         → verify value (use COMPONENT NAMING CONVENTION table)
         → check for unconnected-* pins
         → check flags.dnp = false for mandatory components

STEP 6 : If component not found in STEP 4, use match search
         python scripts\schematic-cli.py query <project> --component --match <name>
         → then verify it connects to correct net from STEP 3

STEP 7 : Apply COMMON FAULT DETECTION RULES F1–F11
         → use PIN MAP functions, NOT hardcoded pin numbers

STEP 8 : Generate report per pin using REVIEW OUTPUT FORMAT
         → only review pins that EXIST in active variant PIN MAP
         → skip pins marked "-" (not available on this variant)
```

### CRITICAL RULES:
- Never assume net names — always discover from STEP 3
- Never hardcode pin numbers — always use PIN MAP functions
- For dual-channel variants, review IN0 and IN1 separately
- Only mark ✅ PASS when component exists + value correct
  + net association verified from query output
- Mark ⚠️ WARNING only when net association cannot be confirmed
  after exhausting STEP 4, 5, and 6

---

## DEVICE VARIANT CONFIGURATION

⚠️ FILL THIS SECTION FIRST before running any review.
All rules and pin checklists use variables defined here.
Update only this section when switching to a different BTS7xx variant.

---

### ACTIVE VARIANT — Edit this before each review session

```
DEVICE_REF        : U1              ← reference in your schematic
DEVICE_PART       : BTS7002-1EPP    ← exact part number
PACKAGE           : 1EPP            ← EPP / EPA / EPZ
CHANNEL_COUNT     : 1               ← 1 = single, 2 = dual channel
```

---

### PIN MAP — Edit pin numbers to match your device datasheet

For each FUNCTION, enter the actual pin number.
Enter  -  if the function does not exist on this variant.

```
FUNCTION          PIN NUMBER    NET DISCOVERY HINTS
──────────────────────────────────────────────────────────────
VS (Exposed Pad)  : EP          VS, VBAT, VSUP, VPOWER, VBB
GND               : 1           GND, PGND, AGND, GND_PWR
IN0               : 2           IN, IN0, INPUT, DIG_IN, GPIO
IN1               : -           IN1, INPUT1, CH2_IN
DEN               : 3           DEN, DIAG_EN, EN_DIAG, DIAG
DSEL              : -           DSEL, SEL, CH_SEL
IS                : 4           IS, IOUT, ISENSE, I_SENSE, CS
OUT_CH1 (all)     : 8,9,10,     OUT, OUTPUT, LOAD, SW, CH1
                    12,13,14
OUT_CH2 (all)     : -           OUT2, CH2, LOAD2
n.c. pins         : 5,6,7,11    (no connection, solder for stability)
```

---

### VARIANT LOOKUP TABLE
Use this table to fill PIN MAP above.
If your variant is not listed, check the datasheet pinout.

```
┌─────────────────┬─────────┬────┬─────┬──────┬─────┬──────────────────┐
│ Part Number     │ Package │ CH │ DEN │ DSEL │ IS  │ OUT pins         │
├─────────────────┼─────────┼────┼─────┼──────┼─────┼──────────────────┤
│ BTS7002-1EPP    │ 1EPP    │ 1  │  3  │  -   │  4  │ 8,9,10,12,13,14  │
│ BTS7004-1EPP    │ 1EPP    │ 1  │  3  │  -   │  4  │ 8,9,10,12,13,14  │
│ BTS7006-1EPP    │ 1EPP    │ 1  │  3  │  -   │  4  │ 8,9,10,12,13,14  │
│ BTS7008-1EPP    │ 1EPP    │ 1  │  3  │  -   │  4  │ 8,9,10,12,13,14  │
│ BTS7010-1EPP    │ 1EPP    │ 1  │  3  │  -   │  4  │ 8,9,10,12,13,14  │
│ BTS7002-2EPP    │ 2EPP    │ 2  │  4  │  5   │  7  │ see datasheet    │
│ BTS7004-2EPP    │ 2EPP    │ 2  │  4  │  5   │  7  │ see datasheet    │
│ BTS7002-1EPA    │ 1EPA    │ 1  │  3  │  -   │  4  │ see datasheet    │
│ BTS7004-1EPA    │ 1EPA    │ 1  │  3  │  -   │  4  │ see datasheet    │
│ BTS7002-2EPA    │ 2EPA    │ 2  │  4  │  5   │  6  │ see datasheet    │
│ BTS7004-2EPA    │ 2EPA    │ 2  │  4  │  5   │  6  │ see datasheet    │
│ BTS7002-1EPZ    │ 1EPZ    │ 1  │  3  │  -   │  4  │ see datasheet    │
│ BTS7004-1EPZ    │ 1EPZ    │ 1  │  3  │  -   │  4  │ see datasheet    │
│ BTS7002-2EPZ    │ 2EPZ    │ 2  │  4  │  5   │  6  │ see datasheet    │
└─────────────────┴─────────┴────┴─────┴──────┴─────┴──────────────────┘
```

---

### DUAL CHANNEL ADDITIONAL RULES
*(Only applies when CHANNEL_COUNT = 2)*

```
IN1  → same rules as IN0 (applied per channel independently)
       Series resistor R_IN1 = 4.7kΩ mandatory
       If unused → 10kΩ pull-down to GND

DSEL → same rules as DEN
       Series resistor R_DSEL = 4.7kΩ mandatory
       If unused → 10kΩ pull-down to GND

IS   → single IS output reports both channels
       Full IS circuit mandatory (same as single channel)

OUT_CH1 and OUT_CH2 → reviewed separately per channel
       Each channel OUT group must share one net
       CH1 and CH2 output nets must NOT be connected together
```

---

## NET DISCOVERY PROTOCOL

⚠️ CRITICAL: Never assume net names.
Net names in the schematic may differ from pin names in this checklist.
Always discover actual net names first before querying for components.

Follow this exact sequence for EVERY pin review:

---

### STEP A — Query BTS7xx IC First

Always start by querying the BTS7xx main IC to get actual net names:

```
python scripts\schematic-cli.py query <project> --component <BTS7xx_ref>
```

From the output, extract the actual net name for each pin:

| Pin | Look for net connected to pin named... |
|-----|----------------------------------------|
| EP  | VS, VSUP, VBAT, V_BAT, VPOWER         |
| 1   | GND, AGND, PGND, GND_PWR              |
| 2   | IN0, IN, INPUT, DIG_IN, GPIO_x        |
| 3   | DEN, DIAG_EN, EN_DIAG, DIAG           |
| 4   | IS, IOUT, ISENSE, I_SENSE, CS         |
| 8–14| OUT, OUTPUT, LOAD, CH1, SW            |

Save these actual net names — use them in all subsequent queries.

---

### STEP B — Query Each Actual Net

After getting actual net names from STEP A, query each net:

```
python scripts\schematic-cli.py query <project> --net <actual_net_name>
```

From output check:
- `pins` list → who is connected to this net
- `pin_count` → how many connections (1 = isolated, should be ≥ 2)
- component references connected → identify passive components

---

### STEP C — Query Each Passive Component Directly

For each passive component found on the net, query it directly:

```
python scripts\schematic-cli.py query <project> --component <ref>
```

Check:
- `value` field → compare against COMPONENT NAMING CONVENTION table
- `nets` list → verify both pins connect to expected nets
- `flags.dnp` → must be false for mandatory components
- any `unconnected-*` net → means floating pin (RULE F1)

---

### STEP D — Use --match as Fallback

If STEP B finds no component on a net, use match search:

```
python scripts\schematic-cli.py query <project> --component --match "R_IN"
python scripts\schematic-cli.py query <project> --component --match "RIN"
python scripts\schematic-cli.py query <project> --component --match "4k7"
```

Then verify the found component connects to the correct net from STEP A.
If it does → ✅ PASS. If it does not → ❌ CRITICAL (wrong placement).

---

### VERIFICATION RULE

A component is only confirmed PASS when ALL three are true:
1. Component exists in schematic (found by query)
2. Component value matches expected (per COMPONENT NAMING CONVENTION)
3. Component is electrically connected to the correct BTS7xx pin net
   (verified via net query, NOT assumed from component name alone)

If condition 3 cannot be verified → status is ⚠️ WARNING with note:
"Net association unconfirmed — run manual verification in KiCad"

---

## REVIEW OUTPUT FORMAT

Use this exact format for every pin:

```
### [Pin Number] — [Pin Name]
**Component Found:** [ref] = [value]
**Status:** ✅ PASS / ❌ CRITICAL / ⚠️ WARNING / 📐 LAYOUT NOTE
**Detail:** [brief explanation]
**Recommendation:** [what to do if not PASS]
```

---

## SCORING CRITERIA

| Finding                                      | Severity    | Action                       |
|----------------------------------------------|-------------|------------------------------|
| Mandatory component missing                  | ❌ CRITICAL | Must fix before release      |
| Wrong component value                        | ❌ CRITICAL | Must fix                     |
| Value within ±10% tolerance                  | ✅ PASS     | Acceptable                   |
| Optional component missing (no placeholder)  | ⚠️ WARNING  | Add placeholder              |
| Layout recommendation not followed          | 📐 NOTE     | Review with layout engineer  |
| Pin is n.c. but not soldered to PCB          | ⚠️ WARNING  | Solder for mechanical stability |

---

## COMPONENT NAMING CONVENTION

In this schematic, passive components may use functional names
instead of actual values in the "Value" field.
Use this mapping table to identify and validate components:

| Value Field Found | Component Type | Expected Value  | Pin Association |
|-------------------|----------------|-----------------|-----------------|
| `R_IN`            | Series resistor on IN0 input     | 4.7kΩ           | Pin 2 — IN0     |
| `R_DEN`           | Series resistor on DEN input     | 4.7kΩ           | Pin 3 — DEN     |
| `R_GND`           | Ground protection resistor       | 47Ω             | Pin 1 — GND     |
| `R_ADC`           | ADC input protection resistor    | 4.7kΩ           | Pin 4 — IS      |
| `R_IS_PROT`       | IS pin protection resistor       | 4.7kΩ           | Pin 4 — IS      |
| `R_SENSE`         | Current sense resistor           | 1.2kΩ (min 820Ω)| Pin 4 — IS      |
| `R_OL`            | Open load pull-up resistor       | 10kΩ            | Pin 8–14 — OUT  |
| `R_PD`            | Pull-down resistor               | 220kΩ           | Pin 8–14 — OUT  |
| `C_VS`            | VS decoupling capacitor          | 100nF           | EP — VS         |
| `C_VSGND`         | VS-GND buffer capacitor          | 47nF            | EP — VS         |
| `C_OUT`           | Output protection capacitor      | 10nF            | Pin 8–14 — OUT  |
| `C_SENSE`         | Sense signal filter capacitor    | 220pF           | Pin 4 — IS      |
| `DZ1`             | Zener diode for ADC protection   | 7V              | Pin 4 — IS      |

### DUAL CHANNEL ADDITIONAL COMPONENTS
*(Only applies when CHANNEL_COUNT = 2)*

| Value Field Found | Component Type              | Expected Value   | Pin Association   |
|-------------------|-----------------------------|------------------|-------------------|
| `R_IN1`           | Series resistor on IN1      | 4.7kΩ            | IN1 pin           |
| `R_DSEL`          | Series resistor on DSEL     | 4.7kΩ            | DSEL pin          |
| `R_IN1_A`         | Limp home resistor 1 on IN1 | 2.2kΩ            | IN1 pin           |
| `R_IN1_B`         | Limp home resistor 2 on IN1 | 2.2kΩ            | IN1 pin           |
| `C_OUT2`          | Output cap channel 2        | 10nF             | OUT_CH2 pins      |

---

### REVIEW RULES FOR NAMED COMPONENTS

**RULE 1 — Component found by functional name → Mark as ✅ PASS (FOUND)**
If the "value" field in the schematic contains a functional name
from the table above (e.g. `R_IN`, `C_VS`), treat the component
as FOUND and correctly identified.

**RULE 2 — Verify reference prefix matches component type**
- Functional name starting with `R_` → reference must start with `R`
- Functional name starting with `C_` → reference must start with `C`
- Functional name starting with `DZ` → reference must start with `D`
- If prefix does not match → mark as ❌ CRITICAL (wrong component type)

**RULE 3 — Add note about value verification**
When a component is identified by functional name only,
always append this note to the finding:

  > ⚠️ Note: Actual component value not confirmed from schematic.
  > Verify that the physical BOM value matches the expected value
  > shown in the table above.

**RULE 4 — Missing component still = CRITICAL**
If neither the functional name NOR a matching value is found
connected to the expected pin net → mark as ❌ CRITICAL as usual.

---

## COMMON FAULT DETECTION RULES

These rules apply to ALL pins during review.
Check every rule for every component found in the schematic.
Rules are evaluated in order — stop at first CRITICAL found per pin.

---

### RULE F1 — Floating Pin (Unconnected Wire)

**How to detect:**
Run `query --component <ref> --full` and check pin-to-net mapping.
A floating pin appears as `unconnected-<ref>-Pad<N>` in the net name.

**Condition:** Any pin shows net name starting with `unconnected-`

**Output:**
```
Status          : ❌ CRITICAL — FLOATING PIN
Detail          : Component <ref> found but pin <N> is not connected
                  to any net. Pin is floating.
                  Floating pins cause unpredictable behavior,
                  fail EMC/ESD requirements, and violate IFX guideline.
Evidence        : pin <N> → net: unconnected-<ref>-Pad<N>
Recommendation  : Connect pin <N> to the correct net via wire in KiCad.
                  Verify wire endpoint touches the pin pad exactly
                  with no gap.
```

---

### RULE F2 — Component Completely Missing

**How to detect:**
Run `query --net <net_name>`.
Check `pin_count` in result — if pin_count = 1, only the IC pin
is on that net, no passive component is present.

**Condition:** Expected component not found on target net AND
pin_count of that net = 1

**Output:**
```
Status          : ❌ CRITICAL — COMPONENT MISSING
Detail          : No <component_type> found on <net_name> net.
                  Net has only 1 connection (IC pin only).
                  Mandatory component is absent from schematic.
Evidence        : query --net <net_name> → pin_count: 1
Recommendation  : Add <component> = <value> per IFX mandatory
                  recommendation. See PIN CHECKLIST for required value.
```

---

### RULE F3 — Isolated Net (One-Side Connection Only)

**How to detect:**
Run `query --component <ref>`.
Check if both pins of a two-terminal component connect to
meaningful nets (not `unconnected-*`).

**Condition:** Component exists but one pin is `unconnected-*`
meaning the component is placed but has no return path.

**Output:**
```
Status          : ❌ CRITICAL — ISOLATED NET
Detail          : <ref> found but forms an open circuit.
                  Pin <A> connects to <net_name> ✅
                  Pin <B> connects to unconnected-<ref>-Pad<B> ❌
                  Component has no return path — non-functional.
Evidence        : query --component <ref> shows one floating pin.
Recommendation  : Connect pin <B> of <ref> to <expected_net>.
                  Verify GND symbol or destination net is placed
                  and wire makes contact with the pin pad.
```

---

### RULE F4 — Unused Pin Not Terminated

**How to detect:**
Run `query --net <pin_net>`.
If pin_count = 1 AND no pull-down/pull-up resistor found nearby,
the pin is unused but not properly terminated.

**Applies to:** IN0 (Pin 2), DEN (Pin 3) only.

**Condition:** Digital input pin has no series resistor AND
no pull-down resistor to GND found on that net.

**Output:**
```
Status          : ⚠️ WARNING — UNTERMINATED UNUSED PIN
Detail          : Digital input pin <name> appears unused.
                  No series resistor and no pull-down found.
                  IFX requires 10kΩ resistor to GND for unused
                  digital input pins to prevent floating state
                  and RF interference.
Evidence        : query --net <net_name> → pin_count: 1, no R found.
Recommendation  : Add 10kΩ pull-down resistor from <pin_net> to GND.
                  Do NOT leave digital input pins floating.
```

---

### RULE F5 — Optional Component Missing (No Placeholder)

**How to detect:**
Search for optional component reference or value name on the
expected net using `query --component --match <name>`.
If no match found, placeholder is absent.

**Condition:** Optional component not found anywhere in schematic
(no DNP placeholder, no component with matching name or value).

**Output:**
```
Status          : ⚠️ WARNING — OPTIONAL PLACEHOLDER MISSING
Detail          : Optional component <name> not found in schematic.
                  IFX recommends designing this as a DNP placeholder
                  on both schematic and PCB layout even if not
                  populated, to allow field rework without PCB respin.
Evidence        : query --component --match <name> → no results.
Recommendation  : Add <component> = <value> marked as DNP
                  (Do Not Populate) in KiCad component properties.
                  Placeholder must also exist on PCB layout.
```

---

### RULE F6 — OUT Pins on Different Nets

**How to detect:**
Run `query --component U1` (BTS7xx reference).
Check net names for pins 8, 9, 10, 12, 13, 14.
All must resolve to the same net name.

**Condition:** Any of pins 8, 9, 10, 12, 13, 14 shows a
different net name from the others.

**Output:**
```
Status          : ❌ CRITICAL — OUT PINS SPLIT ACROSS NETS
Detail          : BTS7xx OUT pins are connected to different nets.
                  IFX requires ALL OUT pins to share one net/copper area
                  because all output pins are internally connected.
                  Split nets create resistance mismatch and current
                  imbalance — risk of localized overheating.
Evidence        : Pin 8  → <net_A>
                  Pin 9  → <net_A>
                  Pin 10 → <net_A>
                  Pin 12 → <net_B>  ❌ DIFFERENT
                  Pin 13 → <net_B>  ❌ DIFFERENT
                  Pin 14 → <net_B>  ❌ DIFFERENT
Recommendation  : Connect all OUT nets together on schematic.
                  On PCB, use single copper area for all OUT pins.
```

---

### RULE F7 — Component Value Outside Tolerance

**How to detect:**
Extract numeric value from component `value` field.
Convert to standard unit (Ω, F, V).
Compare against expected value with ±10% tolerance band.

**Tolerance table:**
| Component   | Expected  | Min (−10%) | Max (+10%) |
|-------------|-----------|------------|------------|
| R_GND       | 47Ω       | 42Ω        | 52Ω        |
| R_IN        | 4.7kΩ     | 4.23kΩ     | 5.17kΩ     |
| R_DEN       | 4.7kΩ     | 4.23kΩ     | 5.17kΩ     |
| R_ADC       | 4.7kΩ     | 4.23kΩ     | 5.17kΩ     |
| R_IS_PROT   | 4.7kΩ     | 4.23kΩ     | 5.17kΩ     |
| R_SENSE     | 1.2kΩ     | 820Ω (min) | no max     |
| C_VS        | 100nF     | 90nF       | 110nF      |
| C_OUT       | 10nF      | 9nF        | 11nF       |
| C_SENSE     | 220pF     | 198pF      | 242pF      |
| C_VSGND     | 47nF      | 42nF       | 52nF       |
| DZ1         | 7V        | 6.3V       | 7.7V       |

**Condition:** Extracted value falls outside Min–Max range.

**Output:**
```
Status          : ❌ CRITICAL — VALUE OUT OF TOLERANCE
Detail          : <ref> = <found_value> is outside acceptable range.
                  Expected: <expected_value> ± 10%
                  Acceptable range: <min> – <max>
                  Found value deviates by <X>% from recommendation.
Evidence        : query --component <ref> → value: <found_value>
Recommendation  : Replace <ref> with <expected_value> from E-series.
                  Nearest standard E24 value: <nearest_e_value>
```

---

### RULE F8 — Mandatory Component Marked DNP

**How to detect:**
Run `query --component <ref>`.
Check `flags` field in result for `"dnp": true`.
Cross-check if this component is in the MANDATORY list for its pin.

**Condition:** Component found with correct value BUT
`flags.dnp = true` AND component is mandatory per PIN CHECKLIST.

**Output:**
```
Status          : ❌ CRITICAL — MANDATORY COMPONENT MARKED DNP
Detail          : <ref> found with correct value <value> BUT
                  component is flagged as DNP (Do Not Populate).
                  This component is MANDATORY per IFX guideline.
                  DNP flag means it will NOT be soldered in production.
Evidence        : query --component <ref> → flags: {dnp: true}
Recommendation  : Remove DNP flag from <ref> in KiCad properties.
                  Right-click component → Properties →
                  uncheck "Do not populate".
```

---

### RULE F9 — Incomplete Sensing Circuit on IS Pin

**How to detect:**
Run `query --net IS` or `query --component --match IS`.
Count how many of the 5 required IS components are present:
R_ADC, C_SENSE, DZ1, R_IS_PROT, R_SENSE.

**Condition:** Between 1–4 of the 5 IS components found
(partial circuit — more dangerous than none because it gives
false confidence while leaving µC unprotected).

**Output:**
```
Status          : ❌ CRITICAL — INCOMPLETE IS SENSING CIRCUIT
Detail          : Partial IS circuit detected.
                  Found    : <list of found components>
                  Missing  : <list of missing components>
                  A partial circuit is worse than no circuit —
                  missing DZ1 leaves µC ADC exposed to overvoltage,
                  missing C_SENSE means RC filter time constant
                  < 1µs requirement (IFX: R_ADC × C_SENSE > 1µs).
Evidence        : Found <N>/5 required IS components on IS net.
Recommendation  : Either complete the full IS circuit:
                    R_ADC = 4.7kΩ, C_SENSE = 220pF, DZ1 = 7V,
                    R_IS_PROT = 4.7kΩ, R_SENSE ≥ 820Ω
                  OR if IS is unused:
                    Remove all partial components and leave IS open.
```

---

### RULE F10 — Same Capacitor Value on VS and OUT Pin

**How to detect:**
Run `query --component --match C` and collect capacitor values
on VS net and OUT net.
Compare values between C_VS and C_OUT.

**Condition:** C_VS and C_OUT have the same capacitance value
(e.g. both 47nF), which IFX explicitly warns against.

**Output:**
```
Status          : ⚠️ WARNING — OSCILLATION RISK (VS/OUT CAP MATCH)
Detail          : C_VS and C_OUT have identical capacitance values.
                  IFX explicitly warns: do NOT use the same cap value
                  on VS and OUT pin — this creates a resonant circuit
                  that can cause oscillation during switching.
Evidence        : C_VS  = <value> on VS net
                  C_OUT = <value> on OUT net
                  Values are identical → oscillation risk.
Recommendation  : Use different values:
                  C_VS  = 100nF (mandatory)
                  C_OUT = 10nF  (mandatory)
                  These differ by 10× — safe combination per IFX.
```

---

### RULE F11 — n.c. Pin Not Soldered to PCB

**How to detect:**
Run `query --component U1 --full`.
Check pins 5, 6, 7, 11 (n.c. pins).
If they show `unconnected-*` net → they are not connected to any net.
This is acceptable electrically but flag if no footprint pad exists.

**Condition:** n.c. pin has `unconnected-*` net AND
component properties show no footprint or footprint has no pad
for that pin number.

**Output:**
```
Status          : ⚠️ WARNING — N.C. PIN MAY LACK PCB PAD
Detail          : Pin <N> is n.c. (not connected internally).
                  IFX recommends soldering n.c. pins to PCB pad
                  for mechanical stability of the package.
                  If PCB footprint omits these pads, package may
                  rock or lift under thermal stress.
Evidence        : pin <N> → unconnected-U1-Pad<N>
Recommendation  : Verify PCB footprint includes pads for pins 5, 6,
                  7, and 11. Pads should be present and soldered
                  even with no electrical connection.
```

---

## PIN CHECKLIST — BTS7xx Smart7

<!--
  ================================================================
  HOW TO ADD A NEW PIN:
  Copy the template block below, paste it after the last pin entry,
  then fill in each field from your Excel columns:
  - PIN_NUMBER   → column "Pin Number"
  - PIN_NAME     → column "Pin Name"
  - DESCRIPTION  → column "Pin Description"
  - HW_MANDATORY → mandatory items from "HW-Recommendation (standard)"
  - HW_OPTIONAL  → optional items from "HW-Recommendation (standard)"
  - FURTHER_INFO → column "Further application specific background"
  - LAYOUT_REC   → column "Layout Recommendation"
  ================================================================

  EMPTY TEMPLATE — COPY FROM HERE:

  ---
  ### [PIN_NUMBER] — [PIN_NAME] | [DESCRIPTION]

  **HW MANDATORY:**
  - `[component]` = [value] — [brief reason]

  **HW OPTIONAL:**
  - `[component]` = [value] — [condition when required]

  **Further Info:**
  > [technical notes from Further Info column]

  **Layout Requirement:**
  - [layout point 1]
  - [layout point 2]

  TO HERE
  ================================================================
-->

---

### EP — VS (Exposed Pad) | Power Supply (Battery Voltage)

**HW MANDATORY:**
- `C_VS` = 100nF — Filter voltage spikes on the battery line,
  improves RF immunity, protects during ESD and BCI events

**HW OPTIONAL:**
- `C_VSGND` = 47nF — Additional buffer cap for fast transients.
  Design as **placeholder** even if not populated.
  Required if: oscillations or retries observed during short-circuit
  test with undervoltage condition

**Further Info:**
> Mind the high current flowing at VS; use PCB area style connection
> instead of trace style connection.
> If short circuit tests with undervoltage have been performed and
> everything was OK (no oscillations, no retries), CVSGND is not needed.
> More details available in Smart7 folder on the community share.

**Layout Requirement:**
- Minimize loop impedance: VS → C_VS → GND
- Place C_VS as close as possible to the exposed pad
- Use **PCB area connection** (not trace) for C_VS solder pads
- Minimum **2 vias** to connect C_VS to PCB GND layer
- Placeholder for C_VSGND **must be present** on PCB layout

---

### 1 — GND | Ground

**HW MANDATORY:**
- `R_GND` = 47Ω — Protection in case of overvoltage and loss of
  battery while driving inductive loads

**HW OPTIONAL:**
- *(none)*

**Further Info:**
> All EMC tests including ISO pulses have been validated with 47 Ohm.
> Higher GND resistance causes GND shift at inverse current condition
> → device may stay OFF or turn OFF unexpectedly.

**Layout Requirement:**
- *(no specific notes)*

---

### [DUAL CHANNEL ONLY] — IN1 | Input Channel 1
*(Skip this pin if CHANNEL_COUNT = 1 or PIN MAP shows IN1 = "-")*

**HW MANDATORY:**
- `R_IN1` = 4.7kΩ series resistor on IN1 input
- If not used: connect with 10kΩ resistor to GND

**HW OPTIONAL:**
- For limp home: split into **2× 2.2kΩ** (R_IN1_A + R_IN1_B)

**Further Info:**
> Same rules as IN0 apply — see IN0 pin entry for full details.

**Layout Requirement:**
- Place R_IN1 as close as possible to BTS IN1 pin

---

### [DUAL CHANNEL ONLY] — DSEL | Channel Select
*(Skip this pin if CHANNEL_COUNT = 1 or PIN MAP shows DSEL = "-")*

**HW MANDATORY:**
- `R_DSEL` = 4.7kΩ series resistor on DSEL pin
- If not used: connect with 10kΩ resistor to GND

**HW OPTIONAL:**
- For limp home: split into **2× 2.2kΩ**

**Further Info:**
> Same rules as DEN apply — digital input pin protection.
> Do NOT apply signal directly to DSEL without series resistor.

**Layout Requirement:**
- Place R_DSEL as close as possible to BTS DSEL pin

---

### [DUAL CHANNEL ONLY] — OUT_CH2 | Output Channel 2
*(Skip this pin if CHANNEL_COUNT = 1 or PIN MAP shows OUT_CH2 = "-")*

**HW MANDATORY:**
- `C_OUT2` = 10nF — protect CH2 output during ESD and BCI
- All CH2 OUT pins must be connected together on PCB
- CH2 net must NOT be connected to CH1 OUT net

**HW OPTIONAL:**
- `R_OL2` = 10kΩ pull-up for open load detection on CH2
- `R_PD2` = 220kΩ pull-down for CH2

**Further Info:**
> Same rules as OUT CH1 apply — see Pin 8 entry for full details.
> CH1 and CH2 are independent outputs — never connect together.

**Layout Requirement:**
- Same layout rules as OUT CH1
- Separate copper area for CH2 from CH1

---

### 2 — IN0 | Input Channel 0

**HW MANDATORY:**
- `R_IN` = 4.7kΩ series resistor on input
- If pin is **not used**: connect with 10kΩ resistor to GND pin
  or module ground

**HW OPTIONAL:**
- For **limp home circuitry**: split 4.7kΩ into **2× 2.2kΩ**
  and apply limp home signal in-between the two resistors
  ⚠️ Do NOT apply limp home signal directly to the digital input pin

**Further Info:**
> Series resistors limit current through pins during ISO pulses or
> Reverse Battery events. 10kΩ is also acceptable.
> Use µC to actively pull down input pin for OFF state to increase
> RF immunity.
> Do not apply limp home signal directly to any digital input pin
> (IN, INx, DEN, DSEL).
> Equivalent resistance of circuitry connected to digital pin must
> be in range of 2.2kΩ – 10kΩ.

**Layout Requirement:**
- Place R_IN as close as possible to the BTS input pin
- Minimizes parasitic capacitance on the input pin

---

### 3 — DEN | Diagnostic Enable (High Active)
*(Digital signal to enable device diagnosis and clear the protection counter of selected channel)*

**HW MANDATORY:**
- `R_DEN` = 4.7kΩ series resistor on DEN pin
- If pin is **not used**: connect with 10kΩ resistor to GND pin
  or module ground

**HW OPTIONAL:**
- For **limp home circuitry**: split 4.7kΩ into **2× 2.2kΩ**
  and apply limp home signal in-between the two resistors
  ⚠️ Do NOT apply limp home signal directly to the digital input pin

**Further Info:**
> Same rules as IN0 (Pin 2) apply here.
> Series resistors limit current through pins during ISO pulses or
> Reverse Battery events. 10kΩ is also acceptable.
> Use µC to actively pull down input pin for OFF state to increase
> RF immunity.
> Equivalent resistance of circuitry connected to digital pin must
> be in range of 2.2kΩ – 10kΩ.

**Layout Requirement:**
- Place R_DEN as close as possible to the BTS input pin
- Minimizes parasitic capacitance on the input pin

---

### 4 — IS | Current Sense Output

**HW MANDATORY:**
- `R_ADC` = 4.7kΩ — Protect µC ADC input during overvoltage,
  reverse polarity and loss of ground
- `C_SENSE` = 220pF — Sense signal filtering
- `DZ1` = 7V Zener diode — Protect µC input during overvoltage
- `R_IS_PROT` = 4.7kΩ — Protection during overvoltage,
  reverse polarity and loss of ground
- `R_SENSE` = 1.2kΩ minimum (min 820Ω) — Limits power losses
  in sense circuitry; application specific value

**HW OPTIONAL:**
- If **pin is not used**: leave open (no connection required)

**Further Info:**
> The RC filter (R_ADC × C_SENSE) must have a time constant > 1µs.
> R_SENSE value: select from E-series resistors, use kILIS Tool for
> calculation. The max. diagnosable load current must correspond to
> max. ADC voltage (usually 5V) to use full dynamic current sense range.

**Layout Requirement:**
- `R_IS_PROT` should be placed close to IS pin
- `R_ADC` and `C_SENSE` should be placed close to µC ADC pin
- Keeps EMC robustness of sense current trace

---

### 5 — n.c. | Not Connected (internally not bonded)

**HW MANDATORY:**
- Solder n.c. pin to PCB — ensures mechanical stability

**HW OPTIONAL:**
- Can be connected to VS, IS, or GND if needed for family concept
  pinout compatibility

**Further Info:**
> The n.c. pins are internally not bonded; there is no conductive
> connection inside the device.
> If it makes sense (family concept), the n.c. pin can be connected
> to VS, IS, or GND.
> Note: 4-channel variant is NOT pin compatible — do not use
> 4-channel pinout as reference.

**Layout Requirement:**
- Ensure PCB footprint has pad for n.c. pin and it is soldered
- See pinout for different family variants (top right of datasheet)

---

### 6 — n.c. | Not Connected (internally not bonded)

**HW MANDATORY:**
- *(no specific requirement listed — treat same as Pin 5)*
- Solder n.c. pin to PCB for mechanical stability (best practice)

**HW OPTIONAL:**
- *(none listed)*

**Further Info:**
> Same rules as Pin 5 apply.

**Layout Requirement:**
- *(no specific notes)*

---

### 7 — n.c. | Not Connected (internally not bonded)

**HW MANDATORY:**
- *(no specific requirement listed — treat same as Pin 5)*
- Solder n.c. pin to PCB for mechanical stability (best practice)

**HW OPTIONAL:**
- *(none listed)*

**Further Info:**
> Same rules as Pin 5 apply.

**Layout Requirement:**
- *(no specific notes)*

---

### 8 — OUT | Output
*(Primary output pin — see also Pins 9, 10, 12, 13, 14)*

**HW MANDATORY:**
- `C_OUT` = 10nF — Protect output during ESD and BCI events
- **All OUT pins (8, 9, 10, 12, 13, 14) MUST be connected together
  on the PCB** — all output pins are internally connected
- PCB traces must be designed to withstand the maximum current

**HW OPTIONAL:**
- `R_OL` (pull-up) = 10kΩ — Enables open load detection at OFF state.
  Switch off pull-up path to reduce standby current.
  *(Datasheet also allows 1.5kΩ but causes higher power loss: 161mW@16V)*
- `R_PD` (pull-down) = 220kΩ — Distinguishes open load from
  short-to-battery in OFF state.
  *(Datasheet also allows 47kΩ)*

**Further Info:**
> Pull-up/pull-down calculation example for Vbat = 12V:
> 12V × 1.5kΩ / (1.5kΩ + 47kΩ) = 0.3V → Below VDS(OLOFF) typ. 1.8V
> → IIS(OLOFF) shown at current sense → indicates Open Load @ OFF state.
>
> ⚠️ Do NOT use the same capacitor value on VS pin and OUT pin
> (e.g. both 47nF) — this may create an oscillation circuit.

**Layout Requirement:**
- Mind the high current flowing at OUT; use **PCB area style
  connection**, not trace style connection
- Minimize loop impedance: OUT → C_OUT → GND
- Place C_OUT as close as possible to the OUT pin
- Use **PCB area connection** (not trace) for C_OUT solder pads
- Minimum **2 vias** to connect C_OUT to PCB GND layer

---

### 9 — OUT | Output
*(Same net as Pins 8, 10, 12, 13, 14 — must all be connected together)*

**HW MANDATORY:**
- Connect to same net as all other OUT pins on PCB
- PCB traces must be designed to withstand the maximum current

**HW OPTIONAL:**
- *(see Pin 8 for output capacitor and pull-up/pull-down details)*

**Further Info:**
> See Pin 8 for full output requirements.

**Layout Requirement:**
- See Pin 8 layout requirements
- All OUT pins connected together on PCB using area-style connection

---

### 10 — OUT | Output
*(Same net as Pins 8, 9, 12, 13, 14 — must all be connected together)*

**HW MANDATORY:**
- Connect to same net as all other OUT pins on PCB
- PCB traces must be designed to withstand the maximum current

**HW OPTIONAL:**
- *(see Pin 8 for output capacitor and pull-up/pull-down details)*

**Further Info:**
> See Pin 8 for full output requirements.

**Layout Requirement:**
- See Pin 8 layout requirements
- All OUT pins connected together on PCB using area-style connection

---

### 11 — n.c. | Not Connected (internally not bonded)

**HW MANDATORY:**
- Solder n.c. pin to PCB — ensures mechanical stability

**HW OPTIONAL:**
- Can be connected to an OUT pin if needed for family concept
  pinout compatibility

**Further Info:**
> The n.c. pins are internally not bonded; there is no conductive
> connection inside the device.
> If it makes sense (family concept), the n.c. pin can be connected
> to an OUT pin.

**Layout Requirement:**
- *(no specific notes)*

---

### 12 — OUT | Output
*(Same net as Pins 8, 9, 10, 13, 14 — must all be connected together)*

**HW MANDATORY:**
- `C_OUT` = 10nF — Protect output during ESD and BCI events
  *(same requirement as Pin 8)*
- **Connect ALL OUT pins (8, 9, 10, 12, 13, 14) together on PCB**
- PCB traces must be designed to withstand the maximum current

**HW OPTIONAL:**
- *(see Pin 8 for pull-up/pull-down details)*

**Further Info:**
> See Pin 8 for full details.
> Confirmed: connect ALL OUT pins 8, 9, 10, 12, 13, 14 together on PCB.

**Layout Requirement:**
- See Pin 8 layout requirements

---

### 13 — OUT | Output
*(Same net as Pins 8, 9, 10, 12, 14 — must all be connected together)*

**HW MANDATORY:**
- Connect to same net as all other OUT pins on PCB
- PCB traces must be designed to withstand the maximum current

**HW OPTIONAL:**
- *(see Pin 8 for output capacitor and pull-up/pull-down details)*

**Further Info:**
> See Pin 8 for full output requirements.

**Layout Requirement:**
- See Pin 8 layout requirements
- All OUT pins connected together on PCB using area-style connection

---

### 14 — OUT | Output
*(Same net as Pins 8, 9, 10, 12, 13 — must all be connected together)*

**HW MANDATORY:**
- Connect to same net as all other OUT pins on PCB
- PCB traces must be designed to withstand the maximum current

**HW OPTIONAL:**
- *(see Pin 8 for output capacitor and pull-up/pull-down details)*

**Further Info:**
> See Pin 8 for full output requirements.

**Layout Requirement:**
- See Pin 8 layout requirements
- All OUT pins connected together on PCB using area-style connection

---

## QUICK REFERENCE SUMMARY

| Pin | Name     | Mandatory Component(s)                                        | Optional / Placeholder        |
|-----|----------|---------------------------------------------------------------|-------------------------------|
| EP  | VS       | C_VS = 100nF                                                  | C_VSGND = 47nF (placeholder)  |
| 1   | GND      | R_GND = 47Ω                                                   | —                             |
| 2   | IN0      | R_IN = 4.7kΩ (or 10kΩ to GND if unused)                      | 2× 2.2kΩ for limp home        |
| 3   | DEN      | R_DEN = 4.7kΩ (or 10kΩ to GND if unused)                     | 2× 2.2kΩ for limp home        |
| 4   | IS       | R_ADC = 4.7kΩ, C_SENSE = 220pF, DZ1 = 7V, R_IS_PROT = 4.7kΩ, R_SENSE = 1.2kΩ | Leave open if unused |
| 5   | n.c.     | Solder to PCB (mechanical stability)                          | Connect to VS/IS/GND if needed|
| 6   | n.c.     | Solder to PCB (best practice)                                 | —                             |
| 7   | n.c.     | Solder to PCB (best practice)                                 | —                             |
| 8   | OUT      | C_OUT = 10nF, all OUT pins connected together                 | R_OL = 10kΩ, R_PD = 220kΩ    |
| 9   | OUT      | Connect to same net as all OUT pins                           | See Pin 8                     |
| 10  | OUT      | Connect to same net as all OUT pins                           | See Pin 8                     |
| 11  | n.c.     | Solder to PCB (mechanical stability)                          | Connect to OUT if needed      |
| 12  | OUT      | C_OUT = 10nF, all OUT pins connected together                 | See Pin 8                     |
| 13  | OUT      | Connect to same net as all OUT pins                           | See Pin 8                     |
| 14  | OUT      | Connect to same net as all OUT pins                           | See Pin 8                     |