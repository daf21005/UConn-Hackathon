import streamlit as st
from dotenv import load_dotenv
from api_client import get_courses, get_grades, upload_syllabus, get_gpa
from gantt import render_gantt
from grades import render_grades

load_dotenv()

st.set_page_config(page_title="SyllabusAI", page_icon="📅", layout="wide")

def sidebar():
    st.sidebar.title("SyllabusAI")
    st.sidebar.caption("Semester planner powered by Gemini")
    st.sidebar.divider()
    student_id = st.sidebar.text_input("Student ID", value="student123")
    st.sidebar.divider()
    st.sidebar.subheader("Upload Syllabus")
    uploaded = st.sidebar.file_uploader("Course syllabus (PDF)", type=["pdf"])
    if uploaded and st.sidebar.button("Parse Syllabus"):
        with st.spinner("Uploading..."):
            result = upload_syllabus(uploaded.read(), uploaded.name)
        if result.get("status") == "mock":
            st.sidebar.info("Backend not connected — using mock data.")
        else:
            st.sidebar.success(f"Parsed: {uploaded.name}")
    st.sidebar.divider()
    page = st.sidebar.radio("View", ["Home", "Gantt Chart", "Grades"])
    return student_id, page

@st.cache_data(ttl=60, show_spinner=False)
def load_data(student_id):
    return get_courses(student_id), get_grades(student_id)

def page_home(courses, grades):
    st.title("Semester Overview")
    total_assignments = sum(len(c.get("assignments", [])) for c in (courses or []))
    gpa_data = get_gpa()
    col1, col2, col3 = st.columns(3)
    col1.metric("Courses",         len(courses) if courses else 0)
    col2.metric("Assignments",     total_assignments)
    col3.metric("Current GPA",     gpa_data.get("gpa", "—"))
    st.divider()
    st.subheader("All assignments")
    import pandas as pd
    rows = []
    for c in (courses or []):
        for a in c.get("assignments", []):
            rows.append({"Course": c["course_name"], "Credits": c.get("credits",3),
                         "Task": a["name"], "Due": a["due_date"],
                         "Weight": f"{a['weight_pct']}%", "Type": a["type"]})
    if rows:
        st.dataframe(pd.DataFrame(rows).sort_values("Due"),
                     use_container_width=True, hide_index=True)
    st.divider()
    st.subheader("Export to Google Calendar")
    if st.button("Export all deadlines"):
        try:
            from calendar_client import push_all_deadlines
            with st.spinner("Connecting..."):
                ok, err = push_all_deadlines(courses or [])
            st.success(f"Exported {ok} deadlines!") if err == 0 else \
            st.warning(f"Exported {ok}, {err} failed — check credentials.json")
        except FileNotFoundError:
            st.error("credentials.json not found. See README for Calendar setup.")
        except ImportError:
            st.error("Run: pip install -r requirements.txt")
        except Exception as e:
            st.error(f"Calendar error: {e}")

def main():
    student_id, page = sidebar()
    if not student_id:
        st.info("Enter a student ID in the sidebar.")
        return
    with st.spinner("Loading data..."):
        courses, grades = load_data(student_id)
    if page == "Home":
        page_home(courses, grades)
    elif page == "Gantt Chart":
        render_gantt(courses)
    elif page == "Grades":
        render_grades(grades)

if __name__ == "__main__":
    main()
