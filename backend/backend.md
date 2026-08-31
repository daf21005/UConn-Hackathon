# SyllabusAI — Backend
### **Status: Complete**


## Run locally
```bash
cd backend/
source ../.venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000

```
Runs at **http://localhost:8000**

To test the endpoints add ```/docs``` at the end of the url.

## .env keys
```
GEMINI_API_KEY=your-key
# The following keys aren't required 
BB_BASE_URL=https://your-bb-instance.edu
BB_APP_KEY=your-key
BB_APP_SECRET=your-secret
```

## Endpoints
```
GET  /                                  health check
GET  /api/student                       current student info
GET  /api/courses/{student_id}          courses + assignments + credits
GET  /api/grades/{student_id}           grade history
GET  /api/gpa                           calculated GPA
GET  /api/courses/{course_id}/recommendation  drop/stay advice
POST /api/upload                        receive syllabus file
POST /api/syllabus/parse                Gemini grade scale extraction
```
