import requests
import os
from dotenv import load_dotenv

load_dotenv()

# pull Blackboard credentials from .env file
BASE_URL = os.getenv("BB_BASE_URL")
APP_KEY = os.getenv("BB_APP_KEY")
APP_SECRET = os.getenv("BB_APP_SECRET")

def get_token():
    response = requests.post(
        f"{BASE_URL}/learn/api/public/v1/oauth2/token",
        data={"grant_type": "client_credentials"},
        auth=(APP_KEY, APP_SECRET)  # sends key and secret as Basic Auth
    )

    # if something goes wrong, print the error and return None
    if response.status_code != 200:
        print(f"Token error: {response.status_code} {response.text}")
        return None

    return response.json()["access_token"]

# helper function - creates autheorization header using out token
def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# Gets basic info about a student using their Blackboard user ID
# Returns name, email, student ID
def get_student_info(user_id):
    token = get_token()
    if not token:
        return None

    response = requests.get(
        f"{BASE_URL}/learn/api/public/v1/users/{user_id}",
        headers=auth_header(token)
    )

    if response.status_code != 200:
        print(f"Student info error: {response.status_code} {response.text}")
        return None
    
    return response.json()


def get_student_courses(user_id):
    token = get_token()
    if not token:
        return None
    
    response = requests.get(
        f"{BASE_URL}/learn/api/public/v1/users/{user_id}/courses",
        headers=auth_header(token)
    )

    if response.status_code != 200:
        print(f"Student courses error: {response.status_code} {response.text}")
        return None

    return response.json()

def get_gradebook_columns(course_id):
    token = get_token()
    if not token:
        return None
    
    response = requests.get(
        f"{BASE_URL}/learn/api/public/v2/courses/{course_id}/gradebook/columns",
        headers=auth_header(token),
        params={
            "fields": "id,name,displayName,score.possible,grading.due,availability.available"
        }
    )

    # we get a back request or conflict
    if response.status_code != 200:
        print(f"Gradebook columns error: {response.status_code} {response.text}")
        return None
    
    return response.json()

def get_student_grade(course_id, column_id, user_id):
    token = get_token()
    if not token:
        return None
    
    response = requests.get(
        f"{BASE_URL}/learn/api/public/v2/courses/{course_id}/gradebook/columns/{column_id}/users/{user_id}",
        headers=auth_header(token)
    )

    if response.status_code != 200:
        print(f"Student grade error: {response.status_code} {response.text}")
        return None
    
    return response.json()

def get_overall_grade(course_id, user_id):
    token = get_token()
    if not token:
        return None
    
    response = requests.get(
        f"{BASE_URL}/learn/api/public/v2/courses/{course_id}/gradebook/users/{user_id}",
        headers=auth_header(token)
    )

    if response.status_code != 200:
        print(f"Overall grade error: {response.status_code} {response.text}")
        return None
    
    return response.json()
