import streamlit as st
import pandas as pd


def render_grades(grades):
    if not grades:
        st.warning("No grade data available.")
        return

    df = pd.DataFrame(grades)
    st.header("Grades")
    st.dataframe(df)

    # TODO: Add more detailed GPA history and grade breakdown visuals.
    try:
        if "semester" in df.columns and "gpa" in df.columns:
            st.subheader("GPA History")
            gpa_by_semester = df.set_index("semester")["gpa"]
            st.line_chart(gpa_by_semester)
        else:
            st.info("GPA history chart will display when semester and gpa fields are provided.")
    except Exception:
        st.error("Unable to render GPA history chart.")
        pass
