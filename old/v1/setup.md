Good update — this changes your frontend quite a bit. You're no longer calling Google APIs directly; your job is now a clean UI layer that talks to FastAPI. Here's the updated picture:Here's what changed and what it means for you:

Your world is now just 5 files. You don't touch Gemini, SQLite, or Blackboard — your teammate owns all of that. Your only connection to the backend is `api_client.py`, which is just Python `requests` calls like `requests.post("http://localhost:8000/upload", files=...)`.

**The one thing to agree on with your teammate right now** — the API contract. You need to know the exact shape of the JSON his endpoints return before you build the Gantt. Ask him to share something like:

```
GET /courses/{student_id}  →  [{course_name, assignments: [{name, due_date, weight_pct, type}]}]
GET /grades/{student_id}   →  [{course, grade, gpa, semester}]
```

Once you have that, you can build the entire frontend independently with fake/mock data and plug in the real API at the end.

**Google Calendar is your Google integration to own** — it lives entirely in your `calendar_client.py` and gives you a strong rubric 3 answer without depending on your teammate at all.

Write `api_client.py` with mock data so we can start building immediately without waiting for the backend
