import os

import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def get_courses(student_id: str):
    try:
        response = requests.get(f"{API_BASE_URL}/courses/{student_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        # TODO: replace this mock with the backend API response format.
        return [
            {
                "course_name": "Sample Course",
                "assignments": [
                    {
                        "name": "Assignment 1",
                        "due_date": "2026-05-01",
                        "start_date": "2026-04-20",
                        "weight_pct": 20,
                        "type": "Homework",
                    },
                    {
                        "name": "Assignment 2",
                        "due_date": "2026-05-08",
                        "start_date": "2026-05-02",
                        "weight_pct": 30,
                        "type": "Project",
                    },
                ],
            }
        ]


def get_grades(student_id: str):
    try:
        response = requests.get(f"{API_BASE_URL}/grades/{student_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        return [
            {
                "course": "Sample Course",
                "grade": "A-",
                "gpa": 3.7,
                "semester": "Spring 2026",
            }
        ]


def upload_file(file_path: str):
    try:
        with open(file_path, "rb") as upload_file:
            response = requests.post(
                f"{API_BASE_URL}/upload",
                files={"file": upload_file},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
    except Exception:
        # TODO: implement upload API contract when backend endpoint is available.
        return {"status": "mock", "message": "Upload API not available in this template."}
