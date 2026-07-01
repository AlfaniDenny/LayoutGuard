---
name: create-pptx
description: Creates professional Infineon-branded PowerPoint presentations using Python and python-pptx with reusable branded components. Use when user asks to create, generate, build, or make a PPTX, PowerPoint, presentation, slide deck, or slides.
---

# Create Infineon PowerPoint Presentation

## Critical Instructions

- **Interpret Intent**: Parse user's request for topic, slide count, style, and content. Ask if unclear.
- **Library**: Use `python-pptx` exclusively. Do NOT use HTML-to-PPTX conversion.
- **Branded Components**: ALWAYS import and use the reusable modules (`infineon_theme`, `slide_builder`, `image_handler`) located alongside this SKILL.md. Never hard-code colors, fonts, or layout positions — use the theme constants.
- **Execution**: Generate AND execute the script — always deliver a `.pptx` file, not just code.
- **Reference Presentations**: Infineon template examples are available in `../../sample_references/` (MC_TPL_* files). Use them for structure and style guidance when creating Infineon-standard presentations.

## Prerequisites

A bundled `python-pptx` v0.6.18 library is included in the `packages/` directory and will be used automatically as a fallback if `python-pptx` is not installed system-wide. For image handling, `Pillow` is still required:

```bash
pip install Pillow
# python-pptx is bundled in packages/ — pip install is optional
```

## Architecture

This skill uses a **hybrid approach**: AI-friendly SKILL.md instructions backed by reusable Python modules.

```
skills/create-pptx/
├── SKILL.md              ← This file (AI reads this)
├── infineon_theme.py     ← Brand colors, fonts, layout constants, slide creators
├── slide_builder.py      ← Pre-built complex layouts (status cards, tables, charts)
├── image_handler.py      ← Image loading, fitting, gallery helpers
├── __init__.py           ← Package init
├── resources/            ← Logo, title images
└── packages/             ← Bundled python-pptx v0.6.18 (fallback)
    └── pptx/             ← python-pptx library
```

## Module Reference

### infineon_theme.py — Theme & Core Slides

#### Constants

```python
from infineon_theme import INFINEON_THEME, hex_to_rgb, _color

# Access colors
C = INFINEON_THEME["colors"]
C["infTeal"]       # "0A8276" — primary brand color
C["infOrange"]     # "F97414" — highlights, in-progress
C["statusGreen"]   # "3B9B91" — completed
C["statusOrange"]  # "F97414" — in progress
C["statusRed"]     # "FF0000" — blocked
C["lightGrey"]     # "F2F2F2" — card backgrounds
C["black"]         # "1D1D1D" — body text

# Access fonts
F = INFINEON_THEME["fonts"]
F["primary"]               # "Arial"
F["sizes"]["titleSlide"]   # 36
F["sizes"]["slideTitle"]   # 24
F["sizes"]["bodyText"]     # 12

# Access layout positions (in inches for 13.333" × 7.5" slides)
L = INFINEON_THEME["layout"]
L["content"]["x"]   # 0.37
L["content"]["y"]   # 1.39
L["content"]["w"]   # 12.60
L["content"]["h"]   # 5.59
```

#### Presentation Factory

```python
from infineon_theme import create_presentation

prs = create_presentation(title="My Deck", author="Sai Kiran Bollu")
# → 13.333" × 7.5" widescreen Presentation object
```

#### Core Slide Creators

```python
from infineon_theme import (
    create_title_slide,
    create_content_slide,
    create_section_slide,
    create_conclusion_slide,
    find_infineon_logo,
)

logo = find_infineon_logo()  # auto-searches common paths, returns str|None

# Title slide (teal key-visual area + title + subtitle)
create_title_slide(prs, "AI Architecture\nfor ATV MC SW",
                   subtitle="ATV MC D SW – Jan 2026",
                   logo_path=logo, key_visual_path="images/hero.jpg")

# Content slide (header + footer, returns slide for adding content)
slide = create_content_slide(prs, "Key Benefits",
                             subtitle="Productivity Improvements",
                             logo_path=logo, page_number=3)

# Section divider (teal background, white title)
create_section_slide(prs, "Part 2: Implementation", logo_path=logo)

# Conclusion / closing slide
create_conclusion_slide(prs, "Summary & Next Steps",
                        bullet_points=["✔ Item 1", "✔ Item 2"],
                        contact_email="sai.kiran@infineon.com",
                        logo_path=logo)
```

#### Low-Level Helpers (for custom layouts)

```python
from infineon_theme import add_textbox, add_shape, add_rich_text

# Simple text box
add_textbox(slide, left=0.5, top=1.5, width=11, height=1,
            text="Hello World", font_size=24, bold=True,
            color="0A8276", alignment=PP_ALIGN.CENTER)

# Shape with fill
from pptx.enum.shapes import MSO_SHAPE
add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE,
          left=1, top=2, width=4, height=3,
          fill_color="E0F2F1", line_color="0A8276", line_width=1)

# Rich text (multiple formatted paragraphs)
add_rich_text(slide, 0.5, 1.5, 11, 4, [
    {"text": "Bold header", "bold": True, "size": 18, "color": "0A8276"},
    {"text": "Normal body text with details..."},
    {"text": "• Bullet item", "bullet": True},
])
```

### slide_builder.py — Pre-Built Layouts

#### Status Card

For project tracking with description, status badge, users, and metrics.

```python
from slide_builder import create_status_card

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_status_card(slide,
    title="Requirements Engineering",
    description=[
        {"text": "REVA – Requirements Evaluation Assistant", "bold": True},
        {"text": "Provides feedback on requirement formulation"},
        {"text": "Continuous delivery until June 2026"},
    ],
    status="Under Development",
    status_color=C["statusOrange"],
    status_details="Browser plug-in infrastructure established",
    users=["6 Beta testers", "CSS 5S, ATV SP", "3 testers from VDF"],
    metrics=[
        {"label": "Cycle Time", "value": "30d", "color": C["infTeal"]},
        {"label": "Effort", "value": "28%", "color": C["infOrange"]},
    ],
    logo_path=logo,
)
```

#### Comparison Table

Multi-column table with styled headers and alternating rows.

```python
from slide_builder import create_comparison_table

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_comparison_table(slide,
    title="AI Paradigm Comparison",
    headers=["Aspect", "Symbolic AI", "Machine Learning", "Gen AI", "Agentic AI"],
    rows=[
        ["Core Function", "Rule-based reasoning", "Pattern analysis", "Content creation", "Autonomous tasks"],
        ["Autonomy", "None", "Low", "Reactive", "High"],
        ["Data Needs", "Manual rules", "Labeled data", "Massive unstructured", "Real-time dynamic"],
    ],
    logo_path=logo,
)
```

#### Architecture Diagram

Horizontal flow with colored boxes, arrows, and callout.

```python
from slide_builder import create_architecture_diagram

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_architecture_diagram(slide,
    title="AI Architecture: Copilot + Agents (MCP)",
    subtitle="Model Context Protocol Integration",
    boxes=[
        {"label": "User\nQuery",     "color": C["blue"],        "subtext": "Natural language"},
        {"label": "GitHub\nCopilot", "color": C["infTeal"],     "subtext": "IDE integration"},
        {"label": "MCP\nServer",     "color": C["accent2"],     "subtext": "Tool routing"},
        {"label": "Knowledge\nGraph","color": C["infOrange"],   "subtext": "RAG + GraphRAG"},
        {"label": "Driver\nCode",    "color": C["statusGreen"], "subtext": "MISRA-compliant"},
    ],
    callout_text="Key insight: secure in-house system with private data via RAG and MCP.",
    logo_path=logo,
)
```

#### Roadmap Timeline

Track-based timeline with phased colored bars.

```python
from slide_builder import create_roadmap

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_roadmap(slide,
    title="Implementation Roadmap",
    subtitle="MC SW AI Tracks – 2025-2026",
    time_labels=["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026"],
    tracks=[
        {"name": "Requirements\nEngineering", "phases": [
            {"label": "REVA Beta",    "color": C["statusGreen"],  "start": 0,   "duration": 1.8},
            {"label": "Prod Rollout", "color": C["infTeal"],      "start": 1.8, "duration": 2.2},
        ]},
        {"name": "Code\nGeneration", "phases": [
            {"label": "POC",          "color": C["statusOrange"], "start": 0,   "duration": 1.0},
            {"label": "Prod SW",      "color": C["infTeal"],      "start": 1.2, "duration": 2.8},
        ]},
    ],
    logo_path=logo,
)
```

#### Two-Column Layout

Problem/solution or concept/example layout.

```python
from slide_builder import create_two_column_layout

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_two_column_layout(slide,
    title='The "Out-of-the-Box" Challenge',
    left_panel={
        "title": "Gen AI\n(Out of the Box)",
        "bg_color": C["infTeal"],
        "items": [
            {"title": "Problem 1: No Context", "text": "• No access to HW datasheets\n• Unknown internal architecture"},
            {"title": "Problem 2: Hallucinations", "text": "• Can make up plausible facts\n• Unacceptable for safety-critical work"},
        ],
    },
    right_panel={
        "title": "IFX Private Data",
        "bg_color": "E0F2F1",
        "items": [
            {"icon": "■", "label": "Datasheets & User Manuals"},
            {"icon": "▲", "label": "SW Architecture Documents"},
            {"icon": "☑", "label": "Coding Standards (MISRA)"},
            {"icon": "⚙", "label": "Register Maps & Errata"},
        ],
    },
    logo_path=logo,
)
```

#### Metric Dashboard

Large KPI numbers in cards.

```python
from slide_builder import create_metric_dashboard

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_metric_dashboard(slide,
    title="Productivity Impact",
    metrics=[
        {"label": "Requirements Analysis", "value": "65%", "color": C["infTeal"], "subtitle": "time reduction"},
        {"label": "Code Generation",       "value": "45%", "color": C["infOrange"], "subtitle": "faster delivery"},
        {"label": "Code Review",           "value": "40%", "color": C["statusGreen"], "subtitle": "cycle time saved"},
    ],
    logo_path=logo,
)
```

#### Image Gallery

```python
from slide_builder import create_image_gallery

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_image_gallery(slide,
    title="System Screenshots",
    images=[
        {"path": "images/screenshot1.png", "caption": "Dashboard View"},
        {"path": "images/screenshot2.png", "caption": "Code Review"},
    ],
    logo_path=logo,
)
```

#### KPI Chart (Planned vs Achieved)

Clustered column chart for tracking planned vs achieved metrics across any categories (quarters, months, sprints, teams, etc.).

```python
from slide_builder import create_kpi_chart

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

# Generic example: quarterly sales targets
create_kpi_chart(slide,
    title="Quarterly Sales - Target vs Actual",
    categories=["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"],
    planned=[100, 120, 140, 160],
    achieved=[95, 118, 145, 155],
    logo_path=logo,
)

# Sprint example:
# create_kpi_chart(slide, title="Sprint Issues", categories=["Sprint 13", "Sprint 14"], ...)
```

#### Effort Chart (Planned vs Delivered)

Clustered column chart for effort/time tracking in days.

```python
from slide_builder import create_effort_chart

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_effort_chart(slide,
    title="Monthly Team Effort (days)",
    categories=["Jan", "Feb", "Mar", "Apr"],
    planned_days=[40.0, 45.0, 42.0, 50.0],
    achieved_days=[38.5, 43.0, 41.5, 48.0],
    logo_path=logo,
)
```

#### Burndown Chart (Stacked)

Stacked column chart showing completed, remaining, and added work. Use `velocity_unit` to customize the annotation label.

```python
from slide_builder import create_burndown_chart

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_burndown_chart(slide,
    title="Project Burndown",
    categories=["Week 1", "Week 2", "Week 3", "Week 4"],
    completed=[10, 15, 20, 25],
    remaining=[50, 40, 28, 12],
    added=[5, 3, 8, 2],
    show_velocity=True,
    velocity_unit="tasks/week",   # default: "items/period"
    logo_path=logo,
)

# Sprint example:
# create_burndown_chart(slide, ..., categories=["Sprint 12", ...], velocity_unit="items/sprint")
```

#### Cumulative Trend Chart (Line)

Line chart for cumulative planned vs achieved trends over time.

```python
from slide_builder import create_cumulative_chart

slide = prs.slides.add_slide(prs.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = hex_to_rgb("FFFFFF")

create_cumulative_chart(slide,
    title="Feature Delivery - Cumulative Trend",
    categories=["Jan", "Feb", "Mar", "Apr"],
    cumulative_planned=[30, 58, 88, 120],
    cumulative_achieved=[28, 54, 83, 113],
    logo_path=logo,
)
```

### image_handler.py — Image Utilities

```python
from image_handler import (
    image_exists,
    get_image_dimensions,
    fit_dimensions,
    center_position,
    load_images_from_directory,
    add_fitted_image,
)

# Check image exists before using
if image_exists("images/diagram.png"):
    w, h = get_image_dimensions("images/diagram.png")
    fit_w, fit_h = fit_dimensions(w, h, max_width=8, max_height=4)

    # Auto-fit and center within bounding box
    add_fitted_image(slide, "images/diagram.png", x=2, y=1.5, max_width=8, max_height=4)

# Load all images from a directory
photos = load_images_from_directory("images/team/")
for photo in photos:
    print(f"{photo['filename']}: {photo['width']}×{photo['height']}")
```

## Creation Workflow

### Step 1: Understand the Request

Extract from the user's description:
- **Topic / Title** — main subject of the presentation
- **Slide Count** — default to 5-8 if not specified
- **Content** — specific points, data, images, quotes to include
- **Audience** — determines tone and complexity

### Step 2: Plan the Slide Deck

Map each slide to a layout type:

| Slide Purpose | Function to Use |
|---|---|
| Opening / title | `create_title_slide()` |
| Section divider | `create_section_slide()` |
| Bullet points / text | `create_content_slide()` + `add_rich_text()` |
| Project status tracking | `create_status_card()` |
| Feature/tech comparison | `create_comparison_table()` |
| System architecture | `create_architecture_diagram()` |
| Project timeline | `create_roadmap()` |
| Problem vs. solution | `create_two_column_layout()` |
| KPI / metrics | `create_metric_dashboard()` |
| Planned vs achieved chart | `create_kpi_chart()` |
| Effort trend chart | `create_effort_chart()` |
| Burndown chart | `create_burndown_chart()` |
| Cumulative trend chart | `create_cumulative_chart()` |
| Photos / screenshots | `create_image_gallery()` |
| Closing / next steps | `create_conclusion_slide()` |

### Step 3: Generate the Script

Always follow this structure:

```python
import sys, os
# Add the skill directory to path so modules can be imported
sys.path.insert(0, "/path/to/skills/create-pptx")

from infineon_theme import (
    INFINEON_THEME, hex_to_rgb, create_presentation,
    create_title_slide, create_content_slide, create_section_slide,
    create_conclusion_slide, find_infineon_logo, add_textbox, add_rich_text,
)
from slide_builder import (
    create_status_card, create_comparison_table,
    create_architecture_diagram, create_roadmap,
    create_two_column_layout, create_metric_dashboard,
    create_kpi_chart, create_effort_chart,
    create_burndown_chart, create_cumulative_chart,
)
from image_handler import image_exists, add_fitted_image

C = INFINEON_THEME["colors"]
L = INFINEON_THEME["layout"]
logo = find_infineon_logo()

prs = create_presentation(title="Your Title", author="Author Name")

# ... add slides using the functions above ...

output_path = "output/my_presentation.pptx"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
prs.save(output_path)
print(f"✔ Saved: {os.path.abspath(output_path)}")
```

### Step 4: Custom Content on Content Slides

When a layout function doesn't fit, use `create_content_slide()` and add custom content:

```python
from pptx.enum.text import PP_ALIGN

slide = create_content_slide(prs, "Custom Slide Title", logo_path=logo)

# Add bullet points
add_rich_text(slide, L["content"]["x"], L["content"]["y"],
              L["content"]["w"], 4.0, [
    {"text": "Key Achievement 1", "bold": True, "size": 16, "color": C["infTeal"]},
    {"text": "Supporting detail for achievement 1", "size": 12},
    {"text": "", "size": 6},  # spacer
    {"text": "Key Achievement 2", "bold": True, "size": 16, "color": C["infTeal"]},
    {"text": "Supporting detail for achievement 2", "size": 12},
])

# Add an image to a content slide
if image_exists("images/chart.png"):
    add_fitted_image(slide, "images/chart.png",
                     x=8, y=1.5, max_width=4.5, max_height=3.5)
```

### Step 5: Charts (python-pptx native)

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

slide = create_content_slide(prs, "Revenue Growth", logo_path=logo)

chart_data = CategoryChartData()
chart_data.categories = ["Q1", "Q2", "Q3", "Q4"]
chart_data.add_series("Revenue ($M)", (100, 150, 200, 250))

slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(1), Inches(1.5), Inches(10), Inches(5),
    chart_data
)
```

### Step 6: Execute and Deliver

1. Run the generated Python script
2. Confirm the `.pptx` file was created
3. Report the **absolute file path** to the user

## Color Reference

All colors are in `INFINEON_THEME["colors"]` — **never hard-code hex values**.

| Name | Hex | Use |
|---|---|---|
| `infTeal` | `0A8276` | Primary brand — titles, headers |
| `infOrange` | `F97414` | Highlights, in-progress |
| `infLime` | `9BBA43` | Success, positive |
| `infYellow` | `FCD442` | Warnings, attention |
| `infMagenta` | `9C216E` | Special accent |
| `statusGreen` | `3B9B91` | Completed / on track |
| `statusOrange` | `F97414` | In progress |
| `statusRed` | `FF0000` | Blocked / critical |
| `black` | `1D1D1D` | Body text |
| `grey` | `8D8786` | Captions, secondary |
| `lightGrey` | `F2F2F2` | Card backgrounds |
| `white` | `FFFFFF` | Slide backgrounds |

## Design Rules

- **Always use blank layout**: `prs.slide_layouts[6]`
- **Always set white background** on new slides before calling builder functions
- **Font**: Arial primary, 36pt titles, 24pt slide titles, 10-12pt body
- **Margins**: min 0.37" from edges
- **Max 6-7 bullet points** per slide
- **Images**: check `image_exists()` before adding; use `add_fitted_image()` for auto-sizing
