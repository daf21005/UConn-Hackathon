"""
generate_slides.py  —  SyllabusAI 10-minute presentation (10 slides)
Run:  python generate_slides.py
Output: slides.pdf  (same folder)

Each slide = 1 landscape page. Edit SLIDES list below to change content.
Timing guide: ~1 min per slide.
"""

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable,
                                 ListFlowable, ListItem, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

OUT = os.path.join(os.path.dirname(__file__), "slides.pdf")
W, H = landscape(letter)   # 11 × 8.5 inches

# ── COLORS ────────────────────────────────────────────────────────────────────
BLUE   = colors.HexColor("#185FA5")
TEAL   = colors.HexColor("#0F6E56")
AMBER  = colors.HexColor("#854F0B")
PURPLE = colors.HexColor("#534AB7")
RED    = colors.HexColor("#A32D2D")
LIGHT  = colors.HexColor("#EEF4FB")
DARK   = colors.HexColor("#2C2C2A")
MID    = colors.HexColor("#5F5E5A")
WHITE  = colors.white

# ── STYLES ────────────────────────────────────────────────────────────────────
def S(name, **kw): return ParagraphStyle(name, **kw)

slide_title_s = S("ST", fontSize=32, textColor=BLUE,  fontName="Helvetica-Bold", spaceAfter=6,  alignment=TA_CENTER)
slide_sub_s   = S("SS", fontSize=14, textColor=MID,   fontName="Helvetica",      spaceAfter=16, alignment=TA_CENTER)
h1_s          = S("H1", fontSize=18, textColor=BLUE,  fontName="Helvetica-Bold", spaceAfter=8,  spaceBefore=4)
h2_s          = S("H2", fontSize=13, textColor=TEAL,  fontName="Helvetica-Bold", spaceAfter=4,  spaceBefore=6)
body_s        = S("B",  fontSize=12, textColor=DARK,  fontName="Helvetica",      leading=18,    spaceAfter=4)
bullet_s      = S("Bl", fontSize=12, textColor=DARK,  fontName="Helvetica",      leading=18)
note_s        = S("N",  fontSize=9,  textColor=MID,   fontName="Helvetica-Oblique", leading=12)
footer_s      = S("F",  fontSize=8,  textColor=MID,   fontName="Helvetica",      alignment=TA_CENTER)
badge_s       = S("Bg", fontSize=11, textColor=WHITE,  fontName="Helvetica-Bold", alignment=TA_CENTER, leading=14)
big_s         = S("Bg2",fontSize=42, textColor=BLUE,  fontName="Helvetica-Bold", alignment=TA_CENTER)
code_s        = S("C",  fontSize=10, textColor=TEAL,  fontName="Courier",        leading=14,    spaceAfter=2)

def h1(t): return Paragraph(t, h1_s)
def h2(t): return Paragraph(t, h2_s)
def p(t):  return Paragraph(t, body_s)
def note(t): return Paragraph(f"<i>{t}</i>", note_s)
def sp(n=8): return Spacer(1, n)
def blist(items, color=BLUE):
    return ListFlowable(
        [ListItem(Paragraph(i, bullet_s), leftIndent=16, bulletColor=color) for i in items],
        bulletType="bullet", leftIndent=12, spaceAfter=4)
def badge(text, col):
    t = Table([[Paragraph(text, badge_s)]], colWidths=[1.6*inch], rowHeights=[0.36*inch])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),col),
                            ("ALIGN",(0,0),(-1,-1),"CENTER"),
                            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                            ("LEFTPADDING",(0,0),(-1,-1),4),
                            ("RIGHTPADDING",(0,0),(-1,-1),4)]))
    return t
def divider(): return HRFlowable(width="100%", thickness=1, color=LIGHT, spaceAfter=8, spaceBefore=4)
def footer(slide_num, timing):
    return Table([[Paragraph(f"SyllabusAI  |  UConn Hackathon 2026", footer_s),
                   Paragraph(f"Slide {slide_num}/10  •  ~{timing}", footer_s)]],
                 colWidths=[4.5*inch, 4.5*inch])

# ── SLIDE BUILDER ─────────────────────────────────────────────────────────────
def slide(content_rows, slide_num, timing):
    """Wrap content in a slide frame with footer."""
    rows = list(content_rows) + [sp(4), divider(), footer(slide_num, timing)]
    return rows + [PageBreak()]

# ── SLIDE CONTENT ─────────────────────────────────────────────────────────────
story = []

# SLIDE 1 — Title
story += slide([
    sp(30),
    Paragraph("SyllabusAI", slide_title_s),
    Paragraph("AI-Powered Semester Gantt Planner", slide_sub_s),
    sp(10),
    Paragraph("Turn your syllabus into a semester strategy", S("T2", fontSize=16, textColor=TEAL,
              fontName="Helvetica-Oblique", alignment=TA_CENTER)),
    sp(20),
    Paragraph("UConn Hackathon 2026  |  Google Vibecoding Event", S("T3", fontSize=12,
              textColor=MID, fontName="Helvetica", alignment=TA_CENTER)),
], 1, "0:00 – 0:45")

# SLIDE 2 — The Problem
story += slide([
    h1("The Problem"),
    divider(),
    sp(4),
    Table([[
        blist([
            "Students juggle 4–5 courses each semester",
            "Every syllabus is a dense wall of text",
            "No unified timeline — exams cluster invisibly",
            "Can't see which assignments actually move the needle",
            "GPA damage happens before students realize it",
        ]),
        sp(1),
        Table([
            [Paragraph("78%", big_s)],
            [Paragraph("of students feel overwhelmed by semester workload", S("q", fontSize=11, textColor=MID, fontName="Helvetica", alignment=TA_CENTER))],
        ], colWidths=[4*inch]),
    ]], colWidths=[5.2*inch, 3.8*inch]),
], 2, "0:45 – 1:45")

# SLIDE 3 — Our Solution
story += slide([
    h1("Our Solution — 3 Steps"),
    divider(),
    sp(8),
    Table([[
        Table([
            [badge("1  Upload", PURPLE)],
            [p("Drop any syllabus PDF into SyllabusAI")],
        ], colWidths=[2.8*inch]),
        Table([
            [badge("2  AI Parses", BLUE)],
            [p("Gemini extracts assignments, dates, and grade weights automatically")],
        ], colWidths=[2.8*inch]),
        Table([
            [badge("3  Visualize", TEAL)],
            [p("Gantt chart + Google Calendar export in seconds")],
        ], colWidths=[2.8*inch]),
    ]], colWidths=[3.0*inch, 3.0*inch, 3.0*inch]),
], 3, "1:45 – 2:45")

# SLIDE 4 — Live Demo
story += slide([
    h1("Live Demo"),
    divider(),
    sp(6),
    p("Walking through the app now:"),
    sp(4),
    blist([
        "Upload a syllabus PDF in the sidebar",
        "Watch Gemini parse assignments and weights",
        "Explore the vGPA-weighted Gantt chart",
        "Filter by course and assignment type",
        "Export all deadlines to Google Calendar with one click",
    ]),
    sp(10),
    note("Demo running at  http://localhost:8501"),
], 4, "2:45 – 5:45")

# SLIDE 5 — The vGPA Feature
story += slide([
    h1("The vGPA Impact System"),
    divider(),
    p("Not all assignments are equal. A 30% exam in a <b>4-credit</b> course matters more than "
      "a 30% exam in a <b>2-credit</b> course."),
    sp(6),
    Table([[
        Table([
            [Paragraph("vGPA Impact Formula", h2_s)],
            [Paragraph("( weight% ÷ 100 ) × course credits", code_s)],
            [sp(4)],
            [p("30% Exam, 4-credit course  →  <b>1.2 vGPA pts</b>")],
            [p("50% Exam, 2-credit course  →  <b>1.0 vGPA pt</b>")],
            [p("10% HW,   3-credit course  →  <b>0.3 vGPA pts</b>")],
        ], colWidths=[4.5*inch]),
        Table([
            [Paragraph("Color Scale", h2_s)],
            [Table([
                [Paragraph("■ Low impact",      S("c", fontSize=11, textColor=colors.HexColor("#1D9E75"), fontName="Helvetica-Bold"))],
                [Paragraph("■ Medium impact",   S("c", fontSize=11, textColor=colors.HexColor("#EF9F27"), fontName="Helvetica-Bold"))],
                [Paragraph("■ High impact",     S("c", fontSize=11, textColor=colors.HexColor("#D85A30"), fontName="Helvetica-Bold"))],
                [Paragraph("■ Critical",        S("c", fontSize=11, textColor=colors.HexColor("#E24B4A"), fontName="Helvetica-Bold"))],
            ], colWidths=[3.5*inch])],
        ], colWidths=[3.5*inch]),
    ]], colWidths=[4.7*inch, 3.8*inch]),
], 5, "5:45 – 6:45")

# SLIDE 6 — Google Tools
story += slide([
    h1("Google Tools Integration"),
    divider(),
    sp(4),
    Table([[
        Table([
            [badge("Gemini API", BLUE)],
            [sp(4)],
            [p("Parses syllabus PDFs into structured JSON: assignment name, due date, weight %, and type")],
            [p("Extracts grade scale (A/B/C thresholds) specific to each professor")],
        ], colWidths=[3.0*inch]),
        Table([
            [badge("Google Calendar", TEAL)],
            [sp(4)],
            [p("Exports every deadline as a calendar event")],
            [p("Color-coded by type: red=Exam, amber=Project, green=HW")],
            [p("Auto-sets 1-day and 3-day popup reminders")],
        ], colWidths=[3.0*inch]),
        Table([
            [badge("Blackboard API", PURPLE)],
            [sp(4)],
            [p("Pulls live course enrollment and current grade data")],
            [p("Pre-populates the dashboard without manual entry")],
        ], colWidths=[3.0*inch]),
    ]], colWidths=[3.1*inch, 3.1*inch, 3.1*inch]),
], 6, "6:45 – 7:30")

# SLIDE 7 — Architecture
story += slide([
    h1("Architecture"),
    divider(),
    sp(6),
    Table([[
        Table([[badge(label, col)] for label, col in [
            ("Student", DARK), ("Streamlit Frontend", PURPLE),
            ("FastAPI Backend", TEAL), ("SQLite Database", AMBER),
        ]], colWidths=[2.5*inch]),
        sp(1),
        Table([[badge(label, col)] for label, col in [
            ("Gemini API", BLUE), ("Google Calendar", BLUE),
            ("Blackboard API", MID), ("Google OAuth 2.0", TEAL),
        ]], colWidths=[2.5*inch]),
    ]], colWidths=[3.5*inch, 0.3*inch, 3.5*inch]),
    sp(12),
    Paragraph("Upload PDF  →  Gemini parse  →  FastAPI + SQLite  →  Streamlit Gantt  →  Google Calendar", code_s),
], 7, "7:30 – 8:15")

# SLIDE 8 — Key Features
story += slide([
    h1("Key Features"),
    divider(),
    Table([[
        blist([
            "vGPA-weighted Gantt chart — heaviest assignments most visible",
            "Color-coded by assignment type across all courses",
            "Filter by course and type — focus on what matters",
            "Danger zone alert — flags top 20% highest-impact items",
        ], BLUE),
        blist([
            "GPA history chart with semester trend line",
            "Drop/Stay recommendation per course",
            "One-click Google Calendar export",
            "Works with mock data — no backend required to demo",
        ], TEAL),
    ]], colWidths=[4.5*inch, 4.5*inch]),
], 8, "8:15 – 8:45")

# SLIDE 9 — Impact
story += slide([
    h1("Impact & Next Steps"),
    divider(),
    Table([[
        Table([
            [h2("Who uses it")],
            [blist(["Any college student with syllabi", "Academic advisors reviewing student load", "Students on academic probation"])],
            [sp(4)],
            [h2("Next Steps")],
            [blist(["Deploy on Google Cloud Run", "Firebase Auth for persistent accounts", "AI drop/stay recommendation engine"])],
        ], colWidths=[4.0*inch]),
        Table([
            [h2("Why it wins on the rubric")],
            [blist([
                "<b>Novel:</b> vGPA impact weighting is new",
                "<b>Well-built:</b> full stack, zero crashes",
                "<b>Google tools:</b> Gemini + Calendar + Blackboard",
                "<b>Presentation:</b> clear problem → solution → demo",
            ])],
        ], colWidths=[4.5*inch]),
    ]], colWidths=[4.2*inch, 4.8*inch]),
], 9, "8:45 – 9:30")

# SLIDE 10 — Q&A
story += slide([
    sp(25),
    Paragraph("Thank You", slide_title_s),
    sp(10),
    Paragraph("Questions?", slide_sub_s),
    sp(16),
    Table([[
        Paragraph("Frontend", S("lbl", fontSize=11, textColor=PURPLE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("Backend", S("lbl2", fontSize=11, textColor=TEAL, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph("Run it", S("lbl3", fontSize=11, textColor=DARK, fontName="Helvetica-Bold", alignment=TA_CENTER)),
    ],
    [
        Paragraph("Streamlit + Plotly", S("val", fontSize=10, textColor=MID, fontName="Helvetica", alignment=TA_CENTER)),
        Paragraph("FastAPI + SQLite + Gemini", S("val2", fontSize=10, textColor=MID, fontName="Helvetica", alignment=TA_CENTER)),
        Paragraph("streamlit run app.py", S("val3", fontSize=10, textColor=MID, fontName="Courier", alignment=TA_CENTER)),
    ]], colWidths=[3.0*inch, 3.0*inch, 3.0*inch]),
], 10, "9:30 – 10:00")

# Remove trailing PageBreak from last slide
if isinstance(story[-1], PageBreak):
    story.pop()

# ── BUILD ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUT, pagesize=landscape(letter),
        leftMargin=0.6*inch, rightMargin=0.6*inch,
        topMargin=0.5*inch,  bottomMargin=0.4*inch)
doc.build(story)
print(f"✓  slides.pdf written to {OUT}  ({len([x for x in story if isinstance(x, PageBreak)])+1} slides)")
