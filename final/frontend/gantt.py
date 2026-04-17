import streamlit as st
import plotly.express as px
import pandas as pd

# vGPA impact = (weight_pct / 100) * course_credits
# e.g. 30% exam in 4-credit course = 1.2 vGPA pts
# e.g. 50% exam in 2-credit course = 1.0 vGPA pt

IMPACT_COLORS = {
    "Low":      "#1D9E75",   # green
    "Medium":   "#EF9F27",   # amber
    "High":     "#D85A30",   # orange
    "Critical": "#E24B4A",   # red
}

TYPE_SYMBOL = {
    "Exam": "⬛", "Project": "◆", "Lab": "●",
    "Homework": "▸", "Quiz": "◇", "Other": "○",
}

def _impact_level(impact: float, max_impact: float) -> str:
    if max_impact == 0:
        return "Low"
    r = impact / max_impact
    if r < 0.4:  return "Low"
    if r < 0.65: return "Medium"
    if r < 0.85: return "High"
    return "Critical"


def _build_df(courses: list) -> pd.DataFrame:
    rows = []
    for course in courses:
        cname   = course.get("course_name", "Unknown")
        credits = course.get("credits", 3)
        for a in course.get("assignments", []):
            due = a.get("due_date", "")
            if not due:
                continue
            start = a.get("start_date") or due
            try:
                s = pd.to_datetime(start)
                e = pd.to_datetime(due)
                if e <= s:
                    e = s + pd.Timedelta(days=1)
            except Exception:
                continue
            wpct   = a.get("weight_pct", 0)
            impact = round((wpct / 100) * credits, 3)
            a_type = a.get("type", "Other")
            sym    = TYPE_SYMBOL.get(a_type, "○")
            rows.append({
                "Course":       cname,
                "Credits":      credits,
                "Task":         f"{sym} {a.get('name','Untitled')}",
                "TaskName":     a.get("name", "Untitled"),
                "Type":         a_type,
                "Start":        s,
                "Finish":       e,
                "Weight (%)":   wpct,
                "vGPA Impact":  impact,
                "Impact Level": "",   # filled after max is known
            })
    df = pd.DataFrame(rows)
    if not df.empty:
        max_i = df["vGPA Impact"].max()
        df["Impact Level"] = df["vGPA Impact"].apply(
            lambda x: _impact_level(x, max_i)
        )
        # Ordered category so legend sorts correctly
        df["Impact Level"] = pd.Categorical(
            df["Impact Level"],
            categories=["Low", "Medium", "High", "Critical"],
            ordered=True,
        )
    return df


def render_gantt(courses):
    if not courses:
        st.warning("No course data available — enter a student ID in the sidebar.")
        return

    st.header("Semester Gantt Chart")

    df = _build_df(courses)
    if df.empty:
        st.info("No assignments with valid dates found.")
        return

    # ── Metrics ───────────────────────────────────────────────────────────────
    total_credits = sum(c.get("credits", 3) for c in courses)
    max_impact    = df["vGPA Impact"].max()
    m1, m2, m3 = st.columns(3)
    m1.metric("Total credits",        total_credits)
    m2.metric("Assignments tracked",  len(df))
    m3.metric("Highest vGPA impact",  f"{max_impact:.2f} pts")

    st.caption(
        "**vGPA impact** = (weight% ÷ 100) × course credits. "
        "A 30% exam in a 4-credit course = **1.2 vGPA pts**. "
        "A 50% exam in a 2-credit course = **1.0 vGPA pt**. "
        "Color shows relative impact: green → amber → orange → red."
    )

    # ── Filters ───────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        sel_courses = st.multiselect(
            "Filter by course",
            options=df["Course"].unique().tolist(),
            default=df["Course"].unique().tolist(),
        )
    with col2:
        sel_types = st.multiselect(
            "Filter by type",
            options=df["Type"].unique().tolist(),
            default=df["Type"].unique().tolist(),
        )

    fdf = df[df["Course"].isin(sel_courses) & df["Type"].isin(sel_types)].copy()
    if fdf.empty:
        st.info("No assignments match the current filters.")
        return

    # ── px.timeline (reliable date rendering) ─────────────────────────────────
    fig = px.timeline(
        fdf,
        x_start="Start",
        x_end="Finish",
        y="Course",
        color="Impact Level",
        color_discrete_map=IMPACT_COLORS,
        category_orders={"Impact Level": ["Low", "Medium", "High", "Critical"]},
        hover_name="TaskName",
        hover_data={
            "Type":        True,
            "Weight (%)":  True,
            "vGPA Impact": True,
            "Credits":     True,
            "Start":       False,
            "Finish":      False,
            "Course":      False,
            "Task":        False,
            "Impact Level":False,
        },
        height=max(380, len(sel_courses) * 100 + 120),
    )

    fig.update_yaxes(autorange="reversed", title="")
    fig.update_xaxes(title="")
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        legend_title_text="vGPA Impact",
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Impact breakdown table ────────────────────────────────────────────────
    with st.expander("vGPA impact breakdown — all assignments"):
        tbl = fdf[["Course", "TaskName", "Type", "Weight (%)", "Credits", "vGPA Impact", "Impact Level"]].copy()
        tbl = tbl.rename(columns={"TaskName": "Assignment"})
        tbl = tbl.sort_values("vGPA Impact", ascending=False)
        st.dataframe(tbl, use_container_width=True, hide_index=True)

    # ── Danger zone ───────────────────────────────────────────────────────────
    danger = fdf[fdf["Impact Level"].isin(["High", "Critical"])].sort_values("Finish")
    if not danger.empty:
        items = ", ".join(
            f"{r['TaskName']} ({r['Course']}, {r['vGPA Impact']:.1f} pts)"
            for _, r in danger.iterrows()
        )
        st.warning(f"**{len(danger)} high-impact assignment(s):** {items}")
