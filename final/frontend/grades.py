import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

GRADE_COLORS = {
    "A": "#1D9E75", "A-": "#5DCAA5",
    "B+": "#378ADD", "B": "#85B7EB", "B-": "#AFA9EC",
    "C+": "#EF9F27", "C": "#FAC775", "C-": "#F0997B",
    "D": "#E24B4A",  "F": "#A32D2D",
}

def render_grades(grades):
    if not grades:
        st.warning("No grade data available — enter a student ID in the sidebar.")
        return

    df = pd.DataFrame(grades)
    st.header("Grades & GPA History")

    if "gpa" in df.columns:
        col1, col2, col3 = st.columns(3)
        col1.metric("Latest GPA",     f"{df['gpa'].iloc[-1]:.2f}")
        col2.metric("Cumulative GPA", f"{df['gpa'].mean():.2f}")
        col3.metric("Highest GPA",    f"{df['gpa'].max():.2f}")

    st.divider()

    if "semester" in df.columns and "gpa" in df.columns:
        st.subheader("GPA by Semester")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["semester"], y=df["gpa"],
            mode="lines+markers",
            line=dict(color="#378ADD", width=2.5),
            marker=dict(size=9, color="#378ADD"),
            hovertemplate="<b>%{x}</b><br>GPA: %{y:.2f}<extra></extra>",
        ))
        fig.add_hline(y=4.0, line_dash="dot", line_color="#B4B2A9", annotation_text="4.0")
        fig.add_hline(y=3.0, line_dash="dot", line_color="#B4B2A9", annotation_text="3.0")
        fig.update_layout(
            yaxis=dict(range=[0, 4.3], title="GPA"),
            xaxis=dict(title=""),
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=280,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    if "grade" in df.columns:
        st.subheader("Course Grades")
        display = df.rename(columns={
            "course": "Course", "grade": "Grade",
            "gpa": "GPA Points", "semester": "Semester",
        })
        def highlight_grade(val):
            return f"color: {GRADE_COLORS.get(str(val), '#888780')}; font-weight: 500;"
        if "Grade" in display.columns:
            st.dataframe(display.style.map(highlight_grade, subset=["Grade"]),
                         use_container_width=True, hide_index=True)
        else:
            st.dataframe(display, use_container_width=True, hide_index=True)

    if "grade" in df.columns and len(df) > 1:
        with st.expander("Grade distribution"):
            gc = df["grade"].value_counts().reset_index()
            gc.columns = ["Grade", "Count"]
            fig2 = px.pie(gc, names="Grade", values="Count",
                          color="Grade", color_discrete_map=GRADE_COLORS, hole=0.4)
            fig2.update_layout(margin=dict(l=10,r=10,t=20,b=10),
                               paper_bgcolor="rgba(0,0,0,0)", height=260)
            st.plotly_chart(fig2, use_container_width=True)
