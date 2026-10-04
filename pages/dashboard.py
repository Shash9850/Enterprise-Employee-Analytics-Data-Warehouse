import pandas as pd
import plotly.express as px
import streamlit as st

from managers.analytics_manager import AnalyticsManager


st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HELPERS
# ============================================================

def format_number(value):
    """Format numeric values with thousands separators."""
    if value is None:
        return "—"
    return f"{int(value):,}"


def safe_float(value, decimals=2):
    """Format a numeric value safely."""
    if value is None:
        return "—"
    return f"{float(value):.{decimals}f}"


def section_title(label, title):
    """Render a consistent dashboard section heading."""
    st.caption(label.upper())
    st.subheader(title)


# ============================================================
# ANALYTICS
# ============================================================

analytics = AnalyticsManager()

try:
    performance_summary = analytics.get_performance_summary()
    yearly_performance = analytics.get_yearly_performance()
    department_performance = analytics.get_department_performance()
    top_employees = analytics.get_top_employees_by_department()

    attrition_summary = analytics.get_attrition_summary()
    attrition_department = analytics.get_attrition_by_department()
    attrition_role = analytics.get_attrition_by_job_role()
    attrition_overtime = analytics.get_attrition_by_overtime()
    attrition_tenure = analytics.get_attrition_by_tenure()
    attrition_risk = analytics.get_attrition_risk_indicators()

    project_attention = analytics.get_project_attention_indicators()
    employee_allocation = analytics.get_employee_allocation()

    scd2_summary = analytics.get_scd2_change_summary()

except Exception as error:
    st.error("Unable to load analytics from the data warehouse.")
    st.exception(error)
    st.stop()


# ============================================================
# DATAFRAMES
# ============================================================

yearly_df = pd.DataFrame(yearly_performance)
department_df = pd.DataFrame(department_performance)
top_employees_df = pd.DataFrame(top_employees)

attrition_department_df = pd.DataFrame(attrition_department)
attrition_role_df = pd.DataFrame(attrition_role)
attrition_overtime_df = pd.DataFrame(attrition_overtime)
attrition_tenure_df = pd.DataFrame(attrition_tenure)
attrition_risk_df = pd.DataFrame(attrition_risk)

project_attention_df = pd.DataFrame(project_attention)
employee_allocation_df = pd.DataFrame(employee_allocation)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 📊 Workforce Intelligence")
    st.caption("Detailed analytics dashboard")

    st.divider()

    st.markdown(
        """
        **Analytics Areas**

        - Performance Intelligence
        - Workforce Intelligence
        - Project Intelligence
        - SCD Type 2 Change Summary
        """
    )

    st.divider()

    st.caption("Powered by the Data Warehouse")


# ============================================================
# HEADER
# ============================================================

st.title("📊 Analytics Dashboard")
st.markdown(
    "Detailed performance, workforce, project, and employee-history "
    "analytics powered by the data warehouse."
)


# ============================================================
# EXECUTIVE KPIs
# ============================================================

section_title("Executive Pulse", "Organization at a glance")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        "Employees",
        format_number(attrition_summary["total_employees"]),
    )

with kpi2:
    st.metric(
        "Performance Reviews",
        format_number(performance_summary["total_reviews"]),
    )

with kpi3:
    st.metric(
        "Projects Reviewed",
        format_number(performance_summary["projects_reviewed"]),
    )

with kpi4:
    st.metric(
        "Average Rating",
        safe_float(performance_summary["average_rating"]),
    )

with kpi5:
    st.metric(
        "Attrition Rate",
        f'{safe_float(attrition_summary["attrition_rate"])}%',
    )


# ============================================================
# PERFORMANCE INTELLIGENCE
# ============================================================

st.divider()
section_title("Performance Intelligence", "Performance activity and trends")

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("**Annual Review Activity**")
    fig = px.bar(
        yearly_df,
        x="year",
        y="total_reviews",
        labels={"year": "Year", "total_reviews": "Reviews"},
    )
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")

with chart2:
    st.markdown("**Annual Average Performance Rating**")
    fig = px.line(
        yearly_df,
        x="year",
        y="average_rating",
        markers=True,
        labels={"year": "Year", "average_rating": "Average Rating"},
    )
    fig.update_yaxes(range=[1, 5])
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")


# Department performance
st.markdown("**Department Performance**")

fig = px.bar(
    department_df,
    x="department_name",
    y="average_rating",
    text="average_rating",
    labels={
        "department_name": "Department",
        "average_rating": "Average Rating",
    },
)
fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
)
fig.update_yaxes(range=[0, 5])
fig.update_layout(
    height=420,
    margin=dict(l=20, r=20, t=30, b=20),
    showlegend=False,
)
st.plotly_chart(fig, width="stretch")


# Top employees
st.markdown("**Top Employees by Department**")
st.caption(
    "Ranked using DENSE_RANK within each department; employees need "
    "at least three reviews to be included."
)

if not top_employees_df.empty:
    st.dataframe(
        top_employees_df[
            [
                "department_name",
                "department_rank",
                "employee_name",
                "review_count",
                "average_rating",
            ]
        ],
        width="stretch",
        hide_index=True,
    )


# ============================================================
# WORKFORCE INTELLIGENCE
# ============================================================

st.divider()
section_title("Workforce Intelligence", "Workforce movement and attrition")

workforce1, workforce2 = st.columns(2)

with workforce1:
    st.markdown("**Attrition by Department**")
    fig = px.bar(
        attrition_department_df,
        x="department_name",
        y="attrition_rate",
        text="attrition_rate",
        labels={
            "department_name": "Department",
            "attrition_rate": "Attrition Rate (%)",
        },
    )
    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")

with workforce2:
    st.markdown("**Attrition by Overtime**")
    fig = px.bar(
        attrition_overtime_df,
        x="overtime",
        y="attrition_rate",
        text="attrition_rate",
        labels={
            "overtime": "Overtime",
            "attrition_rate": "Attrition Rate (%)",
        },
    )
    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")


workforce3, workforce4 = st.columns(2)

with workforce3:
    st.markdown("**Attrition by Job Role**")
    fig = px.bar(
        attrition_role_df.sort_values("attrition_rate"),
        x="attrition_rate",
        y="job_role",
        orientation="h",
        text="attrition_rate",
        labels={
            "job_role": "Job Role",
            "attrition_rate": "Attrition Rate (%)",
        },
    )
    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=40, t=30, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")

with workforce4:
    st.markdown("**Attrition by Tenure**")
    fig = px.bar(
        attrition_tenure_df,
        x="tenure_group",
        y="attrition_rate",
        text="attrition_rate",
        labels={
            "tenure_group": "Tenure",
            "attrition_rate": "Attrition Rate (%)",
        },
    )
    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")


# Risk indicators
st.markdown("**Attrition Risk Indicators**")
st.caption(
    "Rule-based analytical indicators using overtime, tenure, satisfaction, "
    "and work-life-balance fields. These are indicators, not predictions."
)

risk1, risk2 = st.columns([1, 1])

with risk1:
    fig = px.bar(
        attrition_risk_df,
        x="risk_level",
        y="employee_count",
        text="employee_count",
        labels={
            "risk_level": "Risk Indicator",
            "employee_count": "Employees",
        },
    )
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
    )
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig, width="stretch")

with risk2:
    st.dataframe(
        attrition_risk_df[
            [
                "risk_level",
                "employee_count",
                "employees_left",
                "attrition_rate",
            ]
        ],
        width="stretch",
        hide_index=True,
    )


# ============================================================
# PROJECT INTELLIGENCE
# ============================================================

st.divider()
section_title("Project Intelligence", "Project workload and resource indicators")

project1, project2 = st.columns(2)

with project1:
    st.markdown("**Project Attention Indicators**")
    st.caption(
        "Projects are flagged using relative workload, allocation, and "
        "performance indicators."
    )

    if not project_attention_df.empty:
        attention_display = project_attention_df[
            [
                "project_id",
                "project_name",
                "active_employees",
                "total_allocation_percent",
                "average_rating",
                "attention_score",
                "attention_level",
            ]
        ].head(20)

        st.dataframe(
            attention_display,
            width="stretch",
            hide_index=True,
        )

with project2:
    st.markdown("**Attention Level Distribution**")

    if not project_attention_df.empty:
        attention_counts = (
            project_attention_df["attention_level"]
            .value_counts()
            .rename_axis("attention_level")
            .reset_index(name="project_count")
        )

        fig = px.bar(
            attention_counts,
            x="attention_level",
            y="project_count",
            text="project_count",
            labels={
                "attention_level": "Attention Level",
                "project_count": "Projects",
            },
        )
        fig.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
        )
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
            showlegend=False,
        )
        st.plotly_chart(fig, width="stretch")


# Employee allocation
st.markdown("**Current Employee Project Allocation**")
st.caption(
    "Allocation percentage is summed across active projects; it can exceed "
    "100% when an employee is assigned to multiple projects."
)

if not employee_allocation_df.empty:
    st.dataframe(
        employee_allocation_df[
            [
                "employee_id",
                "employee_name",
                "active_project_count",
                "current_allocation_percent",
                "highest_single_allocation",
            ]
        ].head(20),
        width="stretch",
        hide_index=True,
    )


# ============================================================
# SCD TYPE 2 / EMPLOYEE HISTORY
# ============================================================

st.divider()
section_title("Employee History", "SCD Type 2 change summary")

scd1, scd2, scd3 = st.columns(3)

with scd1:
    st.metric(
        "Department Changes",
        format_number(
            scd2_summary["employees_with_department_change"]
        ),
    )

with scd2:
    st.metric(
        "Salary Increases",
        format_number(
            scd2_summary["employees_with_salary_increase"]
        ),
    )

with scd3:
    st.metric(
        "Promotions",
        format_number(
            scd2_summary["employees_with_promotion"]
        ),
    )

st.caption(
    "These figures are derived from changes between SCD Type 2 employee versions."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption(
    "Employee Performance & Workforce Intelligence • "
    "Data Warehouse & Analytics Platform"
)
