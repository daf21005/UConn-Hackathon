# SyllabusAI Hackathon Project

SyllabusAI is a work-in-progress student planning tool built to help organize coursework in one place. The app combines a FastAPI backend with a Streamlit frontend to show courses, grades, GPA information, and assignment timelines in a simple dashboard. It also includes early support for syllabus upload and AI-based grading-scale parsing, plus mock data and placeholder integrations where the full product still needs to be finished.

This is not the final product yet. The project is still being actively worked on, so some pieces are incomplete, mocked, or subject to change as development continues.

## What to run
Use the app in `final/`:
- Backend: FastAPI (`final/backend`)
- Frontend: Streamlit (`final/frontend`)

## Prerequisites
- Python 3.10+
- `pip`

## 1) Set up a virtual environment (from repo root)
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 2) Install dependencies
```bash
python -m pip install -r final/backend/requirements.txt
python -m pip install -r final/frontend/requirements.txt
```

## 3) Run the backend (Terminal 1)
```bash
cd final/backend
python -m uvicorn main:app --reload --port 8000
```

Backend should be available at:
- http://127.0.0.1:8000

## 4) Run the frontend (Terminal 2)
```bash
cd final/frontend
python -m streamlit run app.py --server.port 8501
```

Frontend should be available at:
- http://localhost:8501

## Optional environment variables
For syllabus parsing with Gemini, create a `.env` file in `final/backend/`:
```env
GEMINI_API_KEY=your_key_here
```

If this key is missing, core app pages still run, but AI parsing endpoints may not work.

## Quick test checklist
1. Open http://127.0.0.1:8000 and confirm you see a JSON message.
2. Open http://localhost:8501 and confirm the Streamlit app loads.
3. Navigate Home, Gantt Chart, and Grades pages.
4. (Optional) Try syllabus upload and parsing if `GEMINI_API_KEY` is set.

## Notes
- The `final/` directory is the version intended for demos/testing.
- Older iterations are in `backend/`, `frontend/`, and `old/` for reference.
