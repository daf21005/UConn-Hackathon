"""
generate_report.py  —  SyllabusAI 1-page project summary
Run:  python generate_report.py
Output: report.pdf  (same folder)
Edit the TEXT CONTENT section below to change any wording.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable,
                                 ListFlowable, ListItem)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

OUT = os.path.join(os.path.dirname(__file__), "report.pdf")

# ── COLORS (edit hex values to restyle) ──────────────────────────────────────
BLUE   = colors.HexColor("#185FA5")
TEAL   = colors.HexColor("#0F6E56")
AMBER  = colors.HexColor("#854F0B")
PURPLE = colors.HexColor("#534AB7")
LIGHT  = colors.HexColor("#D3D1C7")
DARK   = colors.HexColor("#2C2C2A")
MID    = colors.HexColor("#5F5E5A")

# ── TEXT CONTENT (edit here) ──────────────────────────────────────────────────
TITLE      = "SyllabusAI"
SUBTITLE   = "AI-Powered Semester Gantt Planner  |  UConn Hackathon 2026"

PROBLEM    = ("Students struggle to visualize workload across multiple courses. "
              "Syllabi are dense PDFs with no timeline, making it hard to anticipate "
              "exam clusters and grade-weight distribution.")

SOLUTION   = ("SyllabusAI lets students upload course syllabi. Gemini extracts every "
              "assignment with its due date and grade weight, then renders a color-coded "
              "Gantt chart spanning the full semester — weighted by vGPA impact.")

FEATURES   = [
    "Color-coded Gantt by assignment type: Exam, Project, HW, Lab, Quiz",
    "vGPA impact weighting: 4-credit exam > 2-credit exam visually",
    "GPA history chart with semester-by-semester trend",
    "Grade table with visual letter-grade coloring",
    "One-click Google Calendar export with reminders",
    "Syllabus PDF upload parsed by Gemini on the backend",
]

GOOGLE_TOOLS = [
    ("<b>Gemini API</b>", "Backend parses syllabus PDFs, extracts structured JSON of assignments, weights, and grade scales."),
    ("<b>Google Calendar API</b>", "Frontend exports all deadlines as color-coded calendar events with 1-day and 3-day reminders."),
    ("<b>Blackboard API</b>", "Backend pulls course enrollment and existing grade data to pre-populate the student dashboard."),
]

STACK      = [
    ("<b>Frontend:</b>", "Streamlit, Plotly, pandas, Python"),
    ("<b>Backend:</b>",  "FastAPI, SQLite, Gemini API, Blackboard API"),
    ("<b>Auth:</b>",     "Google OAuth 2.0 for Calendar integration"),
]

VALUE      = ("Students plan better when workload is visible. SyllabusAI reduces semester "
              "planning to a single upload — turning an opaque PDF into a vGPA-weighted "
              "Gantt timeline that lives in your Google Calendar.")

ARCH_BOXES = [
    ("Student",          DARK),
    ("Streamlit\nUI",    PURPLE),
    ("FastAPI\nBackend", TEAL),
    ("Gemini\nAPI",      BLUE),
    ("SQLite +\nBB API", AMBER),
    ("Google\nCalendar", BLUE),
]
ARCH_CAPTION = ("Upload PDF  →  Gemini parses syllabus  →  FastAPI + SQLite  "
                "→  Streamlit Gantt  →  Google Calendar")

FOOTER_L = "UConn Hackathon  |  Google Vibecoding Event  |  2026"
FOOTER_R = "pip install -r requirements.txt  |  streamlit run app.py"

# ── STYLES ────────────────────────────────────────────────────────────────────
def S(name, **kw): return ParagraphStyle(name, **kw)

title_s  = S("T",  fontSize=22, textColor=BLUE,         fontName="Helvetica-Bold", spaceAfter=2,  alignment=TA_CENTER)
sub_s    = S("Su", fontSize=10, textColor=MID,           fontName="Helvetica",      spaceAfter=6,  alignment=TA_CENTER)
h2_s     = S("H2", fontSize=10, textColor=BLUE,         fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=3)
body_s   = S("B",  fontSize=8.5,textColor=DARK,         fontName="Helvetica",      leading=13,    spaceAfter=3)
bullet_s = S("Bl", fontSize=8.5,textColor=DARK,         fontName="Helvetica",      leading=13)
small_s  = S("Sm", fontSize=7.5,textColor=MID,          fontName="Helvetica",      leading=11)
arch_s   = S("Ar", fontSize=7.5,textColor=colors.white, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=10)

def h(t): return Paragraph(t, h2_s)
def p(t): return Paragraph(t, body_s)
def sp(n=4): return Spacer(1, n)
def blist(items):
    return ListFlowable(
        [ListItem(Paragraph(i, bullet_s), leftIndent=12, bulletColor=BLUE) for i in items],
        bulletType="bullet", leftIndent=8, spaceAfter=3)

# ── BUILD ─────────────────────────────────────────────────────────────────────
doc   = SimpleDocTemplate(OUT, pagesize=letter,
          leftMargin=0.65*inch, rightMargin=0.65*inch,
          topMargin=0.55*inch,  bottomMargin=0.55*inch)
story = []

story += [Paragraph(TITLE, title_s), Paragraph(SUBTITLE, sub_s),
          HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceAfter=8)]

# Two-column layout
left = [h("Problem"), p(PROBLEM), sp(),
        h("Solution"), p(SOLUTION), sp(),
        h("Key Features"), blist(FEATURES)]

right_parts = [h("Google Tools Used")]
for label, desc in GOOGLE_TOOLS:
    right_parts += [p(f"{label} — {desc}"), sp(3)]
right_parts += [sp(), h("Tech Stack")]
for label, val in STACK:
    right_parts.append(p(f"{label} {val}"))
right_parts += [sp(), h("Value Proposition"), p(VALUE)]

two_col = Table([[left, Spacer(0.2*inch,1), right_parts]],
                colWidths=[3.0*inch, 0.2*inch, 3.0*inch])
two_col.setStyle(TableStyle([
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
    ("TOPPADDING",(0,0),(-1,-1),0),  ("BOTTOMPADDING",(0,0),(-1,-1),0),
]))
story.append(two_col)

# Architecture
story += [sp(10), HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=5), h("Architecture")]
arch_cells = [[Paragraph(label, arch_s) for label, _ in ARCH_BOXES]]
arch_table = Table(arch_cells, colWidths=[1.02*inch]*6, rowHeights=[0.42*inch])
cmds = [("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]
for i, (_, col) in enumerate(ARCH_BOXES):
    cmds.append(("BACKGROUND",(i,0),(i,0),col))
arch_table.setStyle(TableStyle(cmds))
story += [arch_table, sp(3), Paragraph(ARCH_CAPTION, small_s)]

# Footer
story += [sp(8), HRFlowable(width="100%", thickness=0.5, color=LIGHT, spaceAfter=4)]
footer = Table([[FOOTER_L, FOOTER_R]], colWidths=[3.1*inch, 3.1*inch])
footer.setStyle(TableStyle([
    ("FONTNAME",(0,0),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),7.5),
    ("TEXTCOLOR",(0,0),(-1,-1),MID),
    ("ALIGN",(0,0),(0,0),"LEFT"),("ALIGN",(1,0),(1,0),"RIGHT"),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
]))
story.append(footer)

doc.build(story)
print(f"✓  report.pdf written to {OUT}")
