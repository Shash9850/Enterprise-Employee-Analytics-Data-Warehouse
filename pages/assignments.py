import streamlit as st
import pandas as pd
from datetime import date

from managers.assignment_manager import AssignmentManager
from models.assignment import Assignment
from managers.employee_manager import EmployeeManager
from managers.project_manager import ProjectManager


st.set_page_config(
    page_title="Project Assignments",
    page_icon="🔗",
    layout="wide",
)


def inject_css():
    st.markdown(
        """
        <style>
        .page-hero {
            padding: 1.35rem 1.6rem;
            border-radius: 18px;
            border: 1px solid rgba(128,128,128,.18);
            background: linear-gradient(135deg, rgba(80,80,120,.10), rgba(80,160,140,.08));
            margin-bottom: 1.2rem;
        }
        .page-hero h1 { margin: 0; font-size: 2rem; }
        .page-hero p { margin: .35rem 0 0; opacity: .72; }
        .section-label {
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
            opacity: .58;
            margin-bottom: .35rem;
        }
        .assignment-note {
            padding: .8rem 1rem;
            border-radius: 12px;
            background: rgba(80,120,180,.08);
            border: 1px solid rgba(80,120,180,.16);
            margin: .5rem 0 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def validate_dates(start_date, end_date):
    if end_date < start_date:
        st.error("End date cannot be earlier than the start date.")
        return False
    return True


def load_employees():
    manager = EmployeeManager()
    employees = manager.get_all_employees()
    return employees


def load_projects():
    manager = ProjectManager()
    projects = manager.get_all_projects()
    return projects


inject_css()

st.markdown(
    """
    <div class="page-hero">
        <div class="section-label">Workforce Operations</div>
        <h1>🔗 Project Assignments</h1>
        <p>Allocate employees to projects, manage assignment periods, and monitor active workforce allocation.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

assignment_manager = AssignmentManager()

try:
    employees = load_employees()
    projects = load_projects()
except Exception as error:
    st.error(f"Unable to load employee or project data: {error}")
    st.stop()

employee_lookup = {
    f"{employee.employee_id} — {employee.first_name} {employee.last_name}": employee
    for employee in employees
}

project_lookup = {
    f"{project.project_id} — {project.project_name}": project
    for project in projects
}

all_details = assignment_manager.get_assignment_details(active_only=False)
active_details = assignment_manager.get_assignment_details(active_only=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Assignments", f"{len(all_details):,}")
col2.metric("Active Assignments", f"{len(active_details):,}")
col3.metric("Employees Assigned", f"{len({r['employee_id'] for r in active_details}):,}")
col4.metric("Active Projects", f"{len({r['project_id'] for r in active_details}):,}")

st.divider()

tab_create, tab_manage, tab_view = st.tabs(
    ["➕ New Assignment", "🛠️ Manage Assignment", "📋 Assignment Register"]
)

with tab_create:
    st.subheader("Create Employee–Project Assignment")
    st.caption("Define who is assigned, to which project, for what allocation, and for which period.")

    with st.form("create_assignment_form", clear_on_submit=True):
        c1, c2 = st.columns(2)

        with c1:
            employee_label = st.selectbox(
                "Employee",
                options=list(employee_lookup.keys()),
                index=None,
                placeholder="Select an employee",
            )

        with c2:
            project_label = st.selectbox(
                "Project",
                options=list(project_lookup.keys()),
                index=None,
                placeholder="Select a project",
            )

        c3, c4, c5 = st.columns(3)
        with c3:
            allocation = st.number_input(
                "Allocation (%)",
                min_value=1,
                max_value=100,
                value=100,
                step=5,
            )
        with c4:
            start_date = st.date_input("Start Date", value=date.today())
        with c5:
            end_date = st.date_input("End Date", value=date.today())

        submitted = st.form_submit_button(
            "Create Assignment",
            type="primary",
            width="stretch",
        )

        if submitted:
            if not employee_label or not project_label:
                st.error("Please select both an employee and a project.")
            elif not validate_dates(start_date, end_date):
                pass
            else:
                employee = employee_lookup[employee_label]
                project = project_lookup[project_label]

                assignment = Assignment(
                    employee_id=employee.employee_id,
                    project_id=project.project_id,
                    allocation_percent=allocation,
                    start_date=start_date,
                    end_date=end_date,
                )

                if assignment_manager.create_assignment(assignment):
                    st.success(
                        f"Assignment created successfully for {assignment.employee_id}."
                    )
                else:
                    st.error("Failed to create assignment.")

with tab_manage:
    st.subheader("Find and Manage Assignment")

    if not all_details:
        st.info("No assignments are available.")
    else:
        assignment_options = {
            f"#{row['assignment_id']} — {row['employee_id']} → "
            f"{row['project_id']} {row['project_name']}": row
            for row in all_details
        }

        selected_label = st.selectbox(
            "Select Assignment",
            options=list(assignment_options.keys()),
            index=None,
            placeholder="Choose an assignment",
        )

        if selected_label:
            selected = assignment_options[selected_label]

            st.markdown(
                f"""
                <div class="assignment-note">
                    <strong>{selected['employee_name']}</strong>
                    &nbsp;→&nbsp;
                    <strong>{selected['project_name']}</strong>
                    &nbsp;·&nbsp;
                    {selected['allocation_percent']}% allocation
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.form("update_assignment_form"):
                c1, c2 = st.columns(2)

                with c1:
                    employee_label_update = st.selectbox(
                        "Employee",
                        options=list(employee_lookup.keys()),
                        index=list(employee_lookup.keys()).index(
                            next(
                                label
                                for label, employee in employee_lookup.items()
                                if employee.employee_id == selected["employee_id"]
                            )
                        ),
                    )

                with c2:
                    project_label_update = st.selectbox(
                        "Project",
                        options=list(project_lookup.keys()),
                        index=list(project_lookup.keys()).index(
                            next(
                                label
                                for label, project in project_lookup.items()
                                if project.project_id == selected["project_id"]
                            )
                        ),
                    )

                c3, c4, c5 = st.columns(3)
                with c3:
                    allocation_update = st.number_input(
                        "Allocation (%)",
                        min_value=1,
                        max_value=100,
                        value=int(selected["allocation_percent"]),
                        step=5,
                    )
                with c4:
                    start_update = st.date_input(
                        "Start Date",
                        value=selected["start_date"],
                        key="assignment_start_update",
                    )
                with c5:
                    end_update = st.date_input(
                        "End Date",
                        value=selected["end_date"],
                        key="assignment_end_update",
                    )

                update_submitted = st.form_submit_button(
                    "Save Changes",
                    type="primary",
                    width="stretch",
                )

                if update_submitted:
                    if not validate_dates(start_update, end_update):
                        st.stop()

                    employee = employee_lookup[employee_label_update]
                    project = project_lookup[project_label_update]

                    assignment = Assignment(
                        assignment_id=selected["assignment_id"],
                        employee_id=employee.employee_id,
                        project_id=project.project_id,
                        allocation_percent=allocation_update,
                        start_date=start_update,
                        end_date=end_update,
                    )

                    if assignment_manager.update_assignment(assignment):
                        st.success("Assignment updated successfully.")
                        st.rerun()
                    else:
                        st.error("Assignment could not be updated.")

            st.divider()

            with st.expander("Danger Zone"):
                st.warning("Deleting an assignment permanently removes this employee-project allocation.")
                if st.button(
                    "Delete Assignment",
                    type="secondary",
                    key=f"delete_{selected['assignment_id']}",
                ):
                    if assignment_manager.delete_assignment(selected["assignment_id"]):
                        st.success("Assignment deleted successfully.")
                        st.rerun()
                    else:
                        st.error("Assignment could not be deleted.")

with tab_view:
    st.subheader("Assignment Register")

    active_only = st.toggle("Show active assignments only", value=True)

    details = (
        assignment_manager.get_assignment_details(active_only=True)
        if active_only
        else all_details
    )

    if details:
        df = pd.DataFrame(details)
        df = df.rename(
            columns={
                "assignment_id": "Assignment ID",
                "employee_id": "Employee ID",
                "employee_name": "Employee",
                "project_id": "Project ID",
                "project_name": "Project",
                "allocation_percent": "Allocation %",
                "start_date": "Start Date",
                "end_date": "End Date",
            }
        )

        st.dataframe(
            df,
            hide_index=True,
            width="stretch",
            column_config={
                "Allocation %": st.column_config.ProgressColumn(
                    "Allocation %",
                    min_value=0,
                    max_value=100,
                    format="%d%%",
                )
            },
        )
    else:
        st.info("No assignments match the selected filter.")
