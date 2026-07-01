"""
Sample Infineon Presentation (Hybrid Approach)

Demonstrates all pre-built layouts from the hybrid skill:
- Title slide with Infineon branding
- Status card layout
- Comparison table
- Architecture diagram
- Roadmap timeline
- Two-column layout
- Metric dashboard
- Content slide with bullets
- Conclusion slide

Run:
    cd skills/create-pptx
    python sample_presentation.py
"""

import sys
import os

# Ensure the skill modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from infineon_theme import (
    INFINEON_THEME, hex_to_rgb,
    create_presentation, create_title_slide, create_content_slide,
    create_section_slide, create_conclusion_slide,
    find_infineon_logo, add_textbox, add_rich_text,
)
from slide_builder import (
    create_status_card, create_comparison_table,
    create_architecture_diagram, create_roadmap,
    create_two_column_layout, create_metric_dashboard,
)

C = INFINEON_THEME["colors"]
L = INFINEON_THEME["layout"]


def main():
    logo = find_infineon_logo()
    prs = create_presentation(
        title="AI Architecture for Automotive MC SW",
        author="Sai Kiran Bollu",
    )

    # ─── SLIDE 1: Title Slide ───
    create_title_slide(
        prs,
        "AI Architecture for\nAutomotive MC SW",
        subtitle="ATV MC D SW – Jan 2026",
        logo_path=logo,
    )

    # ─── SLIDE 2: Status Card ───
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = hex_to_rgb(C["white"])

    create_status_card(slide, page_number=2,
        title="Requirements Engineering",
        description=[
            {"text": "REVA – Requirements Evaluation Assistant", "bold": True},
            {"text": "Provide feedback on requirements formulation"},
            {"text": "Reformulate requirements where gaps are detected"},
            {"text": "Continuous delivery plan until June 2026 (Prod quality)"},
        ],
        status="Under Development",
        status_color=C["statusOrange"],
        status_details="Browser plug-in infrastructure established. Rolled out for testing on 27 Oct 25.",
        users=[
            "6 Beta tester users",
            "CSS 5S, ATV SP",
            "3 additional testers from VDF",
        ],
        metrics=[
            {"label": "Cycle Time", "value": "30d", "color": C["infTeal"]},
            {"label": "Effort",     "value": "28%", "color": C["infOrange"]},
        ],
        logo_path=logo,
    )

    # ─── SLIDE 3: Comparison Table ───
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = hex_to_rgb(C["white"])

    create_comparison_table(slide, page_number=3,
        title="Comparison of AI Paradigms",
        headers=["Aspect", "Symbolic AI", "Machine Learning", "Generative AI", "Agentic AI"],
        rows=[
            ["Core Function", "Reasoning based\non explicit rules", "Analyzing data\nto find patterns", "Creating new\ncontent", "Autonomous\nmulti-step tasks"],
            ["Autonomy Level", "None (programmed)", "Low (defined tasks)", "Reactive (prompts)", "High (minimal\nintervention)"],
            ["Data Requirements", "Structured +\nmanual rules", "Labeled datasets", "Massive\nunstructured data", "Real-time\ndynamic data"],
            ["Applications", "Expert systems,\ndecision trees", "Predictive analytics,\nrecommendations", "Content creation,\nchatbots", "Workflow automation,\ndiscovery"],
            ["Limitation", "Brittle, no\nambiguity handling", "Narrow,\ntask-specific", "Can hallucinate", "Complexity,\nethical risks"],
        ],
        logo_path=logo,
    )

    # ─── SLIDE 4: Architecture Diagram ───
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = hex_to_rgb(C["white"])

    create_architecture_diagram(slide, page_number=4,
        title="AI Architecture: Copilot + Agents (MCP)",
        subtitle="Model Context Protocol Integration",
        boxes=[
            {"label": "User\nQuery",      "color": C["blue"],        "subtext": "Natural language\nrequirement"},
            {"label": "GitHub\nCopilot",  "color": C["infTeal"],     "subtext": "IDE integration\nInline assist"},
            {"label": "MCP\nServer",      "color": C["accent2"],     "subtext": "Tool routing\nContext mgmt"},
            {"label": "Knowledge\nGraph", "color": C["infOrange"],   "subtext": "RAG + GraphRAG\nDatasheets"},
            {"label": "Driver\nCode",     "color": C["statusGreen"], "subtext": "MISRA-compliant\ngenerated code"},
        ],
        callout_text=(
            "Key Insight: We've created a secure in-house system where Copilot is "
            "super-charged with our private data (via RAG) and given new capabilities "
            "(via MCP). The AI has full context of our datasheets, coding standards, "
            "and architecture — while staying within Infineon's network."
        ),
        logo_path=logo,
    )

    # ─── SLIDE 5: Roadmap Timeline ───
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = hex_to_rgb(C["white"])

    create_roadmap(slide, page_number=5,
        title="Implementation Roadmap",
        subtitle="MC SW AI Tracks – 2025-2026",
        time_labels=["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026"],
        tracks=[
            {"name": "Requirements\nEngineering", "phases": [
                {"label": "REVA Beta",    "color": C["statusGreen"], "start": 0,   "duration": 1.8},
                {"label": "Prod Rollout", "color": C["infTeal"],     "start": 1.8, "duration": 2.2},
            ]},
            {"name": "Code\nDocumentation", "phases": [
                {"label": "POC",            "color": C["statusOrange"], "start": 0,   "duration": 1.0},
                {"label": "Reference SW",   "color": C["statusGreen"],  "start": 1.2, "duration": 1.8},
                {"label": "Prod SW",        "color": C["infTeal"],      "start": 3.1, "duration": 1.9},
            ]},
            {"name": "Code\nReview", "phases": [
                {"label": "ACRA Dev",       "color": C["statusOrange"], "start": 0.6, "duration": 1.4},
                {"label": "MCAL Rollout",   "color": C["statusGreen"],  "start": 2.2, "duration": 2.0},
            ]},
            {"name": "Test\nGeneration", "phases": [
                {"label": "POC",            "color": C["statusOrange"], "start": 1.6, "duration": 1.0},
                {"label": "iLLD Pilot",     "color": C["statusGreen"],  "start": 2.8, "duration": 1.6},
            ]},
        ],
        logo_path=logo,
    )

    # ─── SLIDE 6: Two-Column Layout ───
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = hex_to_rgb(C["white"])

    create_two_column_layout(slide, page_number=6,
        title='The "Out-of-the-Box" Challenge',
        left_panel={
            "title": "Generative AI\n(Out of the Box)",
            "bg_color": C["infTeal"],
            "items": [
                {
                    "title": "Problem 1: No Context",
                    "text": "• Trained on public internet only\n• No access to HW datasheets\n• Unknown internal architecture\n• Cannot read coding standards",
                },
                {
                    "title": "Problem 2: Hallucinations",
                    "text": '• Can "make up" plausible facts\n• Code may look correct but be wrong\n• No traceability to sources\n• Unacceptable for safety-critical work',
                },
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
                {"icon": "★", "label": "Historical Bug Database"},
            ],
        },
        logo_path=logo,
    )

    # ─── SLIDE 7: Metric Dashboard ───
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = hex_to_rgb(C["white"])

    create_metric_dashboard(slide, page_number=7,
        title="Productivity Impact",
        metrics=[
            {"label": "Requirements Analysis", "value": "65%", "color": C["infTeal"],     "subtitle": "time reduction"},
            {"label": "Code Generation",       "value": "45%", "color": C["infOrange"],    "subtitle": "faster delivery"},
            {"label": "Code Review",           "value": "40%", "color": C["statusGreen"],  "subtitle": "cycle time saved"},
            {"label": "Test Generation",       "value": "55%", "color": C["infMagenta"],   "subtitle": "faster test creation"},
        ],
        logo_path=logo,
    )

    # ─── SLIDE 8: Content Slide with Bullets ───
    slide = create_content_slide(prs, "Key Benefits",
                                 subtitle="Productivity Improvements",
                                 logo_path=logo, page_number=8)

    add_rich_text(slide, L["content"]["x"], L["content"]["y"],
                  L["content"]["w"], 4.0, [
        {"text": "Requirements Analysis", "bold": True, "size": 16, "color": C["infTeal"]},
        {"text": "60-70% time reduction through automated quality checks and reformulation", "size": 12},
        {"text": "", "size": 8},

        {"text": "Code Generation", "bold": True, "size": 16, "color": C["infTeal"]},
        {"text": "40-50% faster driver implementation with context-aware code generation", "size": 12},
        {"text": "", "size": 8},

        {"text": "Code Review", "bold": True, "size": 16, "color": C["infTeal"]},
        {"text": "40% reduction in review cycle time with MISRA compliance automation", "size": 12},
        {"text": "", "size": 8},

        {"text": "Test Generation", "bold": True, "size": 16, "color": C["infTeal"]},
        {"text": "50-60% faster test case creation with specification-driven generation", "size": 12},
    ])

    # ─── SLIDE 9: Conclusion ───
    create_conclusion_slide(
        prs,
        "Summary & Next Steps",
        bullet_points=[
            "✔  Infineon-branded template system with consistent colors and fonts",
            "✔  Status cards for project tracking with metrics and team displays",
            "✔  Comparison tables for technical evaluations",
            "✔  Architecture diagrams showing system flows",
            "✔  Roadmap timelines with phased colored bars",
            "✔  Two-column layouts for problem/solution presentations",
            "→  Ready for integration with VS Code / Claude workflows",
            "→  Supports text, images, charts, and custom layouts",
        ],
        contact_email="sai.kiran@infineon.com",
        logo_path=logo,
    )

    # ─── Save ───
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "sample_presentation.pptx")
    prs.save(output_path)
    print(f"✔ Generated: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
