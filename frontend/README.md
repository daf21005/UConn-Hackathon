# SyllabusAI — Frontend

AI-powered semester Gantt planner. Upload a syllabus PDF → Gemini extracts assignments → color-coded Gantt chart + Google Calendar export.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

App opens at **http://localhost:8501**. Works immediately with mock data — no backend required.

## Connect to backend

When your teammate's FastAPI server is running, set in `.env`:
```
API_BASE_URL=http://localhost:8000
```

Expected endpoints:
```
GET  /courses/{student_id}  →  [{course_name, assignments: [{name, start_date, due_date, weight_pct, type}]}]
GET  /grades/{student_id}   →  [{course, grade, gpa, semester}]
POST /upload                →  {status, message}
```

## Google Calendar setup (optional)

1. [console.cloud.google.com](https://console.cloud.google.com) → Enable **Google Calendar API**
2. Credentials → Create **OAuth 2.0 Client ID** (Desktop app) → download as `credentials.json`
3. Place `credentials.json` in this folder
4. Click "Export all deadlines" in the app — browser opens for one-time authorization

## File overview

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit app — layout, uploader, home page |
| `gantt.py` | Plotly Gantt chart colored by assignment type |
| `grades.py` | GPA history chart + grade table |
| `api_client.py` | HTTP calls to FastAPI (falls back to mock data) |
| `calendar_client.py` | Google Calendar OAuth + deadline export |
| `report.pdf` | 1-page project summary |
