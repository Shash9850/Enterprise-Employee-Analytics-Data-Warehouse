import textwrap

import pandas as pd
import plotly.express as px
import streamlit as st

from managers.analytics_manager import AnalyticsManager


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Employee Performance & Workforce Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #0f172a;
    }

    /* ---------- Hero ---------- */

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        border-radius: 24px;
        padding: 3rem 3.2rem;
        margin-bottom: 2.5rem;
        color: white;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
    }

    .hero-label {
        color: #93c5fd;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 1rem;
    }

    .hero-description {
        max-width: 850px;
        color: #dbeafe;
        font-size: 1rem;
        line-height: 1.7;
    }

    /* ---------- Section ---------- */

    .section-label {
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-top: 1.5rem;
        margin-bottom: 0.45rem;
    }

    .section-title {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
    }

    /* ---------- KPI cards ---------- */

    .kpi-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 1.5rem;
        min-height: 155px;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05);
    }

    .kpi-label {
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.7rem;
    }

    .kpi-value {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }

    .kpi-description {
        color: #94a3b8;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* ---------- Insight cards ---------- */

    .insight-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.4rem;
        min-height: 145px;
    }

    .insight-title {
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.6rem;
    }

    .insight-value {
        color: #0f172a;
        font-size: 1.7rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }

    .insight-description {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* ---------- Product cards ---------- */

    .product-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 1.6rem;
        min-height: 210px;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05);
    }

    .product-icon {
        font-size: 1.5rem;
        margin-bottom: 0.7rem;
        color: #2563eb;
    }

    .product-title {
        color: #0f172a;
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 0.7rem;
    }

    .product-description {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        padding: 2.5rem 0 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def render_html(html):
    """Render a block of custom HTML in Streamlit."""
    st.html(textwrap.dedent(html).strip())


def format_number(value):
    """Format numeric values with thousands separators."""
    return f"{int(value):,}"


# ============================================================
# DATABASE / ANALYTICS MANAGER
# ============================================================

analytics = AnalyticsManager()


# ============================================================
# LOAD ANALYTICS
# ============================================================

try:
    performance_summary = analytics.get_performance_summary()
    yearly_performance = analytics.get_yearly_performance()
    department_performance = analytics.get_department_performance()
    attrition_summary = analytics.get_attrition_summary()
    attrition_department = analytics.get_attrition_by_department()

except Exception as e:
    st.error("Unable to load analytics from the database.")
    st.exception(e)
    st.stop()


# ============================================================
# NORMALIZE DATAFRAMES
# ============================================================

yearly_df = pd.DataFrame(yearly_performance)
department_df = pd.DataFrame(department_performance)
attrition_df = pd.DataFrame(attrition_department)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 📊 Workforce Intelligence")
    st.caption("Employee analytics platform")

    st.divider()

    st.markdown(
        """
        **Executive Dashboard**

        Organization-wide view of:

        - Performance
        - Workforce movement
        - Project intelligence
        - Employee trends
        """
    )

    st.divider()

    st.caption("Data Warehouse & Analytics Platform")


# ============================================================
# HERO
# ============================================================

render_html(
    """
    <div class="hero">

        <div class="hero-label">
            Executive Analytics Platform
        </div>

        <div class="hero-title">
            Employee Performance & Workforce Intelligence
        </div>

        <div class="hero-description">
            A centralized analytics platform for understanding employee
            performance, workforce movement, project workload, and
            organizational trends.
        </div>

    </div>
    """
)


# ============================================================
# EXECUTIVE PULSE
# ============================================================

render_html(
    """
    <div class="section-label">
        Executive Pulse
    </div>

    <div class="section-title">
        Organization at a glance
    </div>
    """
)


total_employees = attrition_summary["total_employees"]
total_reviews = performance_summary["total_reviews"]
total_projects = performance_summary["projects_reviewed"]
attrition_rate = attrition_summary["attrition_rate"]


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:
    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Total Employees
            </div>

            <div class="kpi-value">
                {format_number(total_employees)}
            </div>

            <div class="kpi-description">
                Employees represented in the current workforce dataset.
            </div>

        </div>
        """
    )


with kpi2:
    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Performance Reviews
            </div>

            <div class="kpi-value">
                {format_number(total_reviews)}
            </div>

            <div class="kpi-description">
                Recorded performance reviews available for analysis.
            </div>

        </div>
        """
    )


with kpi3:
    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Project Portfolio
            </div>

            <div class="kpi-value">
                {format_number(total_projects)}
            </div>

            <div class="kpi-description">
                Projects represented in the performance data.
            </div>

        </div>
        """
    )


with kpi4:
    render_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Attrition Rate
            </div>

            <div class="kpi-value">
                {attrition_rate:.2f}%
            </div>

            <div class="kpi-description">
                Recorded employee attrition across the current workforce.
            </div>

        </div>
        """
    )


# ============================================================
# KEY INDICATORS
# ============================================================

st.write("")

render_html(
    """
    <div class="section-label">
        Executive Pulse
    </div>

    <div class="section-title">
        Key indicators
    </div>
    """
)


avg_rating = performance_summary["average_rating"]
employees_reviewed = performance_summary["employees_reviewed"]
active_employees = attrition_summary["active_employees"]
departed_employees = attrition_summary["employees_left"]


insight1, insight2, insight3 = st.columns(3)


with insight1:
    render_html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Performance Coverage
            </div>

            <div class="insight-value">
                {avg_rating:.2f} / 5
            </div>

            <div class="insight-description">
                Average performance rating across
                {format_number(employees_reviewed)} reviewed employees.
            </div>

        </div>
        """
    )


with insight2:
    render_html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Active Workforce
            </div>

            <div class="insight-value">
                {format_number(active_employees)}
            </div>

            <div class="insight-description">
                Employees currently recorded as active
                in the workforce dataset.
            </div>

        </div>
        """
    )


with insight3:
    render_html(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                Recorded Departures
            </div>

            <div class="insight-value">
                {format_number(departed_employees)}
            </div>

            <div class="insight-description">
                Employees recorded as having left
                the organization.
            </div>

        </div>
        """
    )


# ============================================================
# PERFORMANCE INTELLIGENCE
# ============================================================

st.write("")

render_html(
    """
    <div class="section-label">
        Performance Intelligence
    </div>

    <div class="section-title">
        Performance activity & trends
    </div>
    """
)


chart1, chart2 = st.columns(2)


# ---------- Review Activity ----------

with chart1:

    st.subheader("Review Activity")

    st.caption(
        "Annual distribution of recorded performance reviews"
    )

    fig_reviews = px.bar(
        yearly_df,
        x="year",
        y="total_reviews",
        labels={
            "year": "Year",
            "review_count": "Reviews",
        },
    )

    fig_reviews.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
    )

    st.plotly_chart(
        fig_reviews,
        width="stretch",
    )


# ---------- Average Performance ----------

with chart2:

    st.subheader("Average Performance Rating")

    st.caption(
        "Annual movement in average recorded performance rating"
    )

    fig_rating = px.line(
        yearly_df,
        x="year",
        y="average_rating",
        markers=True,
        labels={
            "year": "Year",
            "average_rating": "Average Rating",
        },
    )

    fig_rating.update_yaxes(
        range=[1, 5],
    )

    fig_rating.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
    )

    st.plotly_chart(
        fig_rating,
        width="stretch",
    )


# ============================================================
# DEPARTMENT PERFORMANCE
# ============================================================

render_html(
    """
    <div class="section-label">
        Performance Intelligence
    </div>

    <div class="section-title">
        Department performance
    </div>
    """
)


fig_department = px.bar(
    department_df,
    x="department_name",
    y="average_rating",
    text="average_rating",
    labels={
        "department": "Department",
        "average_rating": "Average Rating",
    },
)

fig_department.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
)

fig_department.update_yaxes(
    range=[0, 5],
)

fig_department.update_layout(
    height=450,
    margin=dict(l=20, r=20, t=30, b=20),
    showlegend=False,
)

st.plotly_chart(
    fig_department,
    width="stretch",
)


# ============================================================
# WORKFORCE INTELLIGENCE
# ============================================================

render_html(
    """
    <div class="section-label">
        Workforce Intelligence
    </div>

    <div class="section-title">
        Workforce movement
    </div>
    """
)


st.subheader("Attrition by Department")

st.caption(
    "Recorded attrition rate across the current employee population"
)


fig_attrition = px.bar(
    attrition_df,
    x="department_name",
    y="attrition_rate",
    text="attrition_rate",
    labels={
        "department_name": "Department",
        "attrition_rate": "Attrition Rate (%)",
    },
)

fig_attrition.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside",
)

fig_attrition.update_layout(
    height=450,
    margin=dict(l=20, r=20, t=30, b=20),
    showlegend=False,
)

st.plotly_chart(
    fig_attrition,
    width="stretch",
)


# ============================================================
# PLATFORM MODULES
# ============================================================

render_html(
    """
    <div class="section-label">
        Platform Modules
    </div>

    <div class="section-title">
        Explore workforce intelligence
    </div>
    """
)


module1, module2, module3 = st.columns(3)


with module1:
    render_html(
        """
        <div class="product-card">

            <div class="product-icon">
                ★
            </div>

            <div class="product-title">
                Performance Intelligence
            </div>

            <div class="product-description">
                Explore performance trends, department results,
                review activity, and top-performing employees.
            </div>

        </div>
        """
    )


with module2:
    render_html(
        """
        <div class="product-card">

            <div class="product-icon">
                ↗
            </div>

            <div class="product-title">
                Workforce Intelligence
            </div>

            <div class="product-description">
                Analyze attrition, workforce risk, tenure,
                overtime patterns, and employee trends.
            </div>

        </div>
        """
    )


with module3:
    render_html(
        """
        <div class="product-card">

            <div class="product-icon">
                ◆
            </div>

            <div class="product-title">
                Project Intelligence
            </div>

            <div class="product-description">
                Understand project workload, resource allocation,
                performance, and potential attention areas.
            </div>

        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        Employee Performance & Workforce Intelligence
        &nbsp;•&nbsp;
        Data-driven workforce analytics platform
    </div>
    """
)