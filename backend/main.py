from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, save_student, save_course, save_gpa_history, save_course_weights, get_student as db_get_student
from dotenv import load_dotenv
import os, json
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from google.genai.errors import APIError

from contextlib import asynccontextmanager

load_dotenv()

class SyllabusText(BaseModel):
    text: str

class GradeTier(BaseModel):
    letter: str = Field(description="Letter grade, e.g., 'A', 'B+', 'Pass'")
    min_pct: float = Field(description="Minimum percentage threshold")
    max_pct: float = Field(description="Maximum percentage threshold")

class SyllabusGradingScale(BaseModel):
    grading_scale: list[GradeTier]

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="SyllabusAI Backend", lifespan=lifespan)

# 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://localhost:5173",
        "http://127.0.0.1:8501",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# MOCK DATA - used for testing purposes

MOCK_STUDENT = {"id": 1, "name": "John", "blackboard_id": "student_001"}

MOCK_COURSES = [
    {
        "id":1,
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
        "id":2,
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
        "id":3,
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
        "id":4,
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
    {"course": "Calculus III",      "grade": "B+", "gpa": 3.3, "semester": "Spring 2026"},
    {"course": "Cybersecurity",     "grade": "D",  "gpa": 1.3, "semester": "Spring 2026"},
    {"course": "Systems Programming","grade": "A", "gpa": 4.0, "semester": "Spring 2026"},
    {"course": "Linear Algebra",    "grade": "C",  "gpa": 2.0, "semester": "Spring 2026"},
]

"""
Use this grading scale for reference when parsing syllabi with Gemini. The AI model may return inconsistent formats, so ensure the output matches expected letter grades and percentage thresholds.
"Grading Scale: A: 93-100, A-: 90-92, B+: 87-89, B: 83-86, B-: 80-82, C+: 77-79, C: 73-76, C-: 70-72, D: 60-69, F: below 60"
"""

# ENDPOINTS

@app.get("/")
def root():
    return {"message": "SyllabusAI backend is running"}

#
@app.get("/api/student")
def get_student_endpoint():
    save_student(
        MOCK_STUDENT["name"], MOCK_STUDENT["blackboard_id"]
    )
    return MOCK_STUDENT

# 
@app.get("/api/courses/{student_id}")
def get_courses(student_id: str):
    student = db_get_student(student_id)

    if student:
        for course in MOCK_COURSES:
            save_course(
                student["id"], course["course_name"], course["credits"], course["current_grade"]
            )
    return MOCK_COURSES

# 
@app.get("/api/grades/{student_id}")
def get_grades(student_id: str):
    student = db_get_student(student_id)

    if student:
        for grade in MOCK_GRADES:
            save_gpa_history(
                student["id"], grade["semester"], grade["gpa"]
            )
    return MOCK_GRADES

@app.get("/api/courses/{course_id}/recommendation")
def get_recommendation(course_id: int):
    course = next((c for c in MOCK_COURSES if c.get("id") == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    grade = course["current_grade"]
    if grade >= 70:
        return {"course_name": course["course_name"], "current_grade": grade,
                "recommendation": "Stay",
                "reason": f"Your grade of {grade}% is passing. You can recover from here."}
    return {"course_name": course["course_name"], "current_grade": grade,
            "recommendation": "Consider Dropping",
            "reason": f"Your grade of {grade}% is below 70%. Dropping protects your GPA."}

@app.get("/api/gpa")
def calculate_gpa():
    def grade_to_points(g):
        if g >= 93: return 4.0
        elif g >= 90: return 3.7
        elif g >= 87: return 3.3
        elif g >= 83: return 3.0
        elif g >= 80: return 2.7
        elif g >= 77: return 2.3
        elif g >= 73: return 2.0
        elif g >= 70: return 1.7
        elif g >= 67: return 1.3
        elif g >= 63: return 1.0
        elif g >= 60: return 0.7
        else: return 0.0

    total_points  = sum(grade_to_points(c["current_grade"]) * c["credits"] for c in MOCK_COURSES)
    total_credits = sum(c["credits"] for c in MOCK_COURSES)
    return {"gpa": round(total_points / total_credits, 2), "total_credits": total_credits}

@app.post("/api/upload")
async def upload_syllabus(file: UploadFile = File(...)):
    contents = await file.read()
    # Pass raw text to Gemini parser — extend here to use PDF extraction
    return {"status": "ok", "filename": file.filename, "size_bytes": len(contents),
            "message": "File received. Connect to /api/syllabus/parse for AI extraction."}

# bug: Gemini will return incorrect letter grade scale ex. "B plus", "B+\n", "B+\",""
# solution: find a way to filter/validate the output to ensure it matches expected letter grades (A, A-, B+, etc.)
@app.post("/api/syllabus/parse")
async def parse_syllabus(payload: SyllabusText):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set in .env")

    client = genai.Client(api_key=api_key)
    # can change Gemini Flash model to any other available models
    # currently set to latest model automatically updated by Google
    target_model = "gemini-flash-latest"

    try:
        response = client.models.generate_content(
            model=target_model,
            contents=[
                "Extract the complete letter grade scale and percentage thresholds from this syllabus text.",
                payload.text
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SyllabusGradingScale,
            ),
        )

        parsed = json.loads(response.text)

        for entry in parsed.get("grading_scale", []):
            save_course_weights(
                course_id=1,
                category=entry["letter"],
                weight_percentage=entry["max_pct"],
                current_score=entry["min_pct"]
            )

        return {"status": "success", "result": parsed}

    except APIError as e:
        raise HTTPException(
            status_code=e.code if e.code else 500,
            detail=f"Gemini API Error ({e.code}): {e.message}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
