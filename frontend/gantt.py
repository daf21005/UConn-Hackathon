import streamlit as st
import plotly.express as px
import pandas as pd


def render_gantt(courses):
    if not courses:
        st.warning("No course data available for the Gantt chart.")
        return

    tasks = []
    for course in courses:
        course_name = course.get("course_name", "Unknown Course")
        for assignment in course.get("assignments", []):
            tasks.append({
                "Task": f"{course_name} - {assignment.get('name', 'Untitled')}",
                "Start": assignment.get("start_date", ""),
                "Finish": assignment.get("due_date", ""),
                "Weight": assignment.get("weight_pct", 0),
            })

    if not tasks:
        st.info("No assignment data available for the chart.")
        return

    df = pd.DataFrame(tasks)

    try:
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Weight")
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.error("Gantt chart rendering is not implemented yet.")
        # TODO: implement full Plotly timeline rendering with validated dates
        pass
