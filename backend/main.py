from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_connection
import google.generativeai as genai
from dotenv import load_dotenv
import os

import json
from pydantic import BaseModel

# will be used for Gemini 
class SyllabusText(BaseModel):
    text: str

# creating the fastAPI app
app = FastAPI()

# load API keys from .env
load_dotenv()

# will be changed
# tells fastapi to accept requests
# assuming the frontend is running on port 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# initializes the database on startup
@app.on_event("startup")
def startup():
    init_db()


# mock data
# THIS IS ALL FAKE DATA 
mock_student = {
    "id": 1,
    "name": "John",
    "blackboard_id": "student_001"
}

mock_courses = [
    {"id": 1, "course_name": "Calculus III",     "credits": 4, "current_grade": 88.5},
    {"id": 2, "course_name": "Cybersecurity",     "credits": 3, "current_grade": 64.0},
    {"id": 3, "course_name": "Systems Programming","credits": 3, "current_grade": 91.2},
    {"id": 4, "course_name": "Linear Algebra",    "credits": 3, "current_grade": 73.5},
]


# basic check - just confirms the backend is running
# visit http://localhost:8000/ to test
@app.get("/")
def root():
    return {"message": "Backend is running"}


# returns the current student's info
# frontend calls this to know who is logged in
@app.get("/api/student")
def get_student():
    return mock_student


# returns all courses and grades for the student
# frontend calls this to build the course dashboard
@app.get("/api/courses")
def get_courses():
    return mock_courses

# drop/stay calc
# returns whether the student should drop or stay
# example: GET /api/courses/2/recommendation
@app.get("/api/courses/{course_id}/recommendation")
def get_recommendation(course_id: int):
    # find the course in our mock data
    course = next((c for c in mock_courses if c["id"] == course_id), None)

    if not course:
        return {"error": "Course not found"}
    
    grade = course["current_grade"]

    if grade >= 70:
        recommendation = "Stay"
        reason = f"Your grade of {grade}% is passing. You can recover from here"
    else:
        recommendation = "Consider Dropping"
        reason = f"Your grade of {grade}% is below 70% dropping the course will protect your GPA"

    return {
        "course_name": course["course_name"],
        "current_grade": grade,
        "recommendation": recommendation,
        "reason": reason
    }

@app.get("/api/gpa")
def calculate_gpa():
    # following uconn gpa (this will be altered)
    def grade_to_points(grade):
        if grade >= 93:   return 4.0
        elif grade >= 90: return 3.7
        elif grade >= 87: return 3.3
        elif grade >= 83: return 3.0
        elif grade >= 80: return 2.7
        elif grade >= 77: return 2.3
        elif grade >= 73: return 2.0
        elif grade >= 70: return 1.7
        elif grade >= 67: return 1.3
        elif grade >= 63: return 1.0
        elif grade >= 60: return 0.7
        else:             return 0.0

    
    total_points = sum(
        grade_to_points(c["current_grade"]) * c["credits"]
        for c in mock_courses
    )
    total_credits = sum(c["credits"] for c in mock_courses)

    gpa = round(total_points / total_credits, 2)

    return {"gpa": gpa, "total_credits": total_credits}

@app.post("/api/syllabus/parse")
async def parse_syllabus(payload: SyllabusText):
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # Note: gemini-1.5-flash is the current standard model name for text tasks
    model = genai.GenerativeModel("gemini-3.1-flash")

    prompt = """
    Extract the grading scale from this syllabus.
    Return JSON only, no explanation, no markdown, in this exact format:
    {
        "grading_scale": [
            {"letter": "A",  "min": 90, "max": 100},
            {"letter": "B",  "min": 80, "max": 89},
            {"letter": "C",  "min": 70, "max": 79},
            {"letter": "D",  "min": 60, "max": 69},
            {"letter": "F",  "min": 0,  "max": 59}
        ]
    }
    """

    # pass the copy-pasted text
    response = model.generate_content([prompt, payload.text])

    # strip away any markdown formatting Gemini might sneak in
    raw_text = response.text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text.removeprefix("```json").removesuffix("```").strip()
    elif raw_text.startswith("```"):
        raw_text = raw_text.removeprefix("```").removesuffix("```").strip()

    # parse it safely into a Python dictionary before returning it to React
    try:
        clean_json = json.loads(raw_text)
        return {"result": clean_json}
    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response into valid JSON", "raw": raw_text}