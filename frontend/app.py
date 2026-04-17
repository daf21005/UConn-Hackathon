import streamlit as st

from api_client import get_courses, get_grades
from gantt import render_gantt
from grades import render_grades

st.set_page_config(page_title="UConn Hackathon", layout="wide")


def load_data(student_id: str):
    if not student_id:
        st.sidebar.warning("Enter a student ID to load data.")
        return None, None

    courses = get_courses(student_id)
    grades = get_grades(student_id)
    return courses, grades


def main():
    st.title("UConn Hackathon Frontend")
    page = st.sidebar.selectbox("Navigation", ["Home", "Gantt", "Grades"])
    student_id = st.sidebar.text_input("Student ID", value="student123")

    courses, grades = load_data(student_id)

    if page == "Home":
        st.header("Welcome")
        st.markdown("Use the sidebar to choose a page and load a student record.")
        if courses is not None:
            st.write("Sample course data:", courses)
    elif page == "Gantt":
        render_gantt(courses)
    elif page == "Grades":
        render_grades(grades)


if __name__ == "__main__":
    main()
