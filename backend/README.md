# SyllabusAI — Backend

## Run locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Runs at **http://localhost:8000**

## .env required keys
```
GEMINI_API_KEY=your-key
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
