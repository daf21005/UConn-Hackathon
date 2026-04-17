from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_connection
import google.generativeai as genai
from dotenv import load_dotenv
import os

# creating the fastAPI app
app = FastAPI()

# load API keys from .env
load_dotenv()

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