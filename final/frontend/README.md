# SyllabusAI — Frontend

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Opens at **http://localhost:8501**. Runs with mock data if backend is offline.

## Connect to backend
In `.env` set `API_BASE_URL=http://localhost:8000`

## API contract (what backend must return)
```
GET  /api/courses/{student_id}  →  [{course_name, credits, current_grade, assignments: [{name, start_date, due_date, weight_pct, type}]}]
GET  /api/grades/{student_id}   →  [{course, grade, gpa, semester}]
GET  /api/gpa                   →  {gpa, total_credits}
POST /api/upload                →  {status, filename, message}
```

## Google Calendar (optional)
Place `credentials.json` from Google Cloud Console in this folder. First export click opens browser auth.
