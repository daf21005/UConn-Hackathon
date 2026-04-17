import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# ── Mock data (used when backend is unreachable) ──────────────────────────────
# Shape must match backend /api/courses/{student_id} exactly.
# credits field is required for vGPA impact calculation in the Gantt chart.

MOCK_COURSES = [
    {
        "course_name": "Calculus III",
        "credits": 4,
        "current_grade": 88.5,
        "assignments": [
            {"name": "HW 1",    "start_date": "2026-01-20", "due_date": "2026-01-27", "weight_pct": 5,  "type": "Homework"},
            {"name": "HW 2",    "start_date": "2026-02-03", "due_date": "2026-02-10", "weight_pct": 5,  "type": "Homework"},
            {"name": "Quiz 1",  "start_date": "2026-02-14", "due_date": "2026-02-14", "weight_pct": 5,  "type": "Quiz"},
            {"name": "Midterm", "start_date": "2026-03-08", "due_date": "2026-03-10", "weight_pct": 30, "type": "Exam"},
            {"name": "HW 3",    "start_date": "2026-03-17", "due_date": "2026-03-24", "weight_pct": 5,  "type": "Homework"},
            {"name": "Project", "start_date": "2026-04-01", "due_date": "2026-04-18", "weight_pct": 20, "type": "Project"},
            {"name": "Final",   "start_date": "2026-05-03", "due_date": "2026-05-05", "weight_pct": 30, "type": "Exam"},
        ],
    },
    {
        "course_name": "Cybersecurity",
        "credits": 3,
        "current_grade": 64.0,
        "assignments": [
            {"name": "Lab 1",   "start_date": "2026-01-22", "due_date": "2026-01-29", "weight_pct": 10, "type": "Lab"},
            {"name": "Lab 2",   "start_date": "2026-02-12", "due_date": "2026-02-19", "weight_pct": 10, "type": "Lab"},
            {"name": "Midterm", "start_date": "2026-03-11", "due_date": "2026-03-13", "weight_pct": 25, "type": "Exam"},
            {"name": "Lab 3",   "start_date": "2026-04-02", "due_date": "2026-04-09", "weight_pct": 15, "type": "Lab"},
            {"name": "Final",   "start_date": "2026-05-06", "due_date": "2026-05-08", "weight_pct": 40, "type": "Exam"},
        ],
    },
    {
        "course_name": "Systems Programming",
        "credits": 3,
        "current_grade": 91.2,
        "assignments": [
            {"name": "HW 1",    "start_date": "2026-01-27", "due_date": "2026-02-03", "weight_pct": 8,  "type": "Homework"},
            {"name": "HW 2",    "start_date": "2026-02-17", "due_date": "2026-02-24", "weight_pct": 8,  "type": "Homework"},
            {"name": "Midterm", "start_date": "2026-03-14", "due_date": "2026-03-16", "weight_pct": 29, "type": "Exam"},
            {"name": "HW 3",    "start_date": "2026-03-30", "due_date": "2026-04-06", "weight_pct": 8,  "type": "Homework"},
            {"name": "Project", "start_date": "2026-04-07", "due_date": "2026-04-28", "weight_pct": 17, "type": "Project"},
            {"name": "Final",   "start_date": "2026-05-09", "due_date": "2026-05-11", "weight_pct": 30, "type": "Exam"},
        ],
    },
    {
        "course_name": "Linear Algebra",
        "credits": 3,
        "current_grade": 73.5,
        "assignments": [
            {"name": "HW 1",    "start_date": "2026-01-21", "due_date": "2026-01-28", "weight_pct": 10, "type": "Homework"},
            {"name": "Quiz 1",  "start_date": "2026-02-11", "due_date": "2026-02-11", "weight_pct": 5,  "type": "Quiz"},
            {"name": "Midterm", "start_date": "2026-03-09", "due_date": "2026-03-11", "weight_pct": 35, "type": "Exam"},
            {"name": "HW 2",    "start_date": "2026-04-01", "due_date": "2026-04-08", "weight_pct": 10, "type": "Homework"},
            {"name": "Final",   "start_date": "2026-05-07", "due_date": "2026-05-09", "weight_pct": 40, "type": "Exam"},
        ],
    },
]

MOCK_GRADES = [
    {"course": "Calculus III",       "grade": "B+", "gpa": 3.3, "semester": "Spring 2026"},
    {"course": "Cybersecurity",      "grade": "D",  "gpa": 1.3, "semester": "Spring 2026"},
    {"course": "Systems Programming","grade": "A",  "gpa": 4.0, "semester": "Spring 2026"},
    {"course": "Linear Algebra",     "grade": "C",  "gpa": 2.0, "semester": "Spring 2026"},
]

# ── API calls ─────────────────────────────────────────────────────────────────

def get_courses(student_id: str):
    """GET /api/courses/{student_id} — returns list with assignments + credits."""
    try:
        r = requests.get(f"{API_BASE_URL}/api/courses/{student_id}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return MOCK_COURSES


def get_grades(student_id: str):
    """GET /api/grades/{student_id} — returns grade + GPA list."""
    try:
        r = requests.get(f"{API_BASE_URL}/api/grades/{student_id}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return MOCK_GRADES


def upload_syllabus(file_bytes: bytes, filename: str):
    """POST /api/upload — send syllabus PDF to backend for Gemini parsing."""
    try:
        r = requests.post(
            f"{API_BASE_URL}/api/upload",
            files={"file": (filename, file_bytes, "application/pdf")},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return {"status": "mock", "message": "Backend not connected — using mock data."}


def get_gpa():
    """GET /api/gpa — returns calculated GPA and total credits."""
    try:
        r = requests.get(f"{API_BASE_URL}/api/gpa", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {"gpa": 2.71, "total_credits": 13}
