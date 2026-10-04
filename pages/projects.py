import streamlit as st

from managers.project_manager import ProjectManager
from models.project import Project


st.title("Project Management")

st.write(
    "Create, search, update, and manage project information "
    "from the workforce database."
)

st.divider()


# ============================================================
# CREATE PROJECT
# ============================================================

st.subheader("Create Project")

col1, col2 = st.columns(2)

with col1:
    project_name = st.text_input(
        "Project Name",
        placeholder="Example: Employee Analytics Platform"
    )

    department_id = st.number_input(
        "Department ID",
        min_value=1,
        max_value=3,
        value=1,
        step=1
    )

    start_date = st.date_input(
        "Start Date"
    )

with col2:
    budget = st.number_input(
        "Budget",
        min_value=0.0,
        value=10000.0,
        step=1000.0
    )

    status = st.selectbox(
        "Status",
        ["Planned", "Active", "Completed", "On Hold"]
    )

    end_date = st.date_input(
        "End Date"
    )


if st.button("Create Project", type="primary"):

    if not project_name.strip():
        st.error("Project name is required.")

    elif end_date < start_date:
        st.error("End date cannot be before start date.")

    elif budget <= 0:
        st.error("Budget must be greater than 0.")

    else:
        project = Project(
            project_id=None,
            project_name=project_name.strip(),
            department_id=department_id,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            status=status
        )

        manager = ProjectManager()
        success = manager.create_project(project)

        if success:
            st.success(
                "Project created successfully."
            )
        else:
            st.error(
                "Project could not be created. "
                "Please check the database or project details."
            )


st.divider()


# ============================================================
# FIND PROJECT
# ============================================================

st.subheader("Find Project")

search_project_id = st.number_input(
    "Project ID",
    min_value=1,
    step=1,
    value=1,
    key="search_project_id"
)

if st.button("Search Project", type="primary"):

    manager = ProjectManager()

    project = manager.get_project(search_project_id)

    if project is None:
        st.warning(
            f"No project found with Project ID {search_project_id}."
        )

    else:
        st.success("Project found.")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Project ID:**", project.project_id)
            st.write("**Project Name:**", project.project_name)
            st.write("**Department ID:**", project.department_id)
            st.write("**Start Date:**", project.start_date)

        with col2:
            st.write("**End Date:**", project.end_date)
            st.write("**Budget:**", project.budget)
            st.write("**Status:**", project.status)


st.divider()


# ============================================================
# UPDATE PROJECT
# ============================================================

st.subheader("Update Project")

update_project_id = st.number_input(
    "Project ID to Update",
    min_value=1,
    step=1,
    value=1,
    key="update_project_id"
)

if st.button("Load Project", key="load_project"):

    manager = ProjectManager()

    project = manager.get_project(update_project_id)

    if project is None:
        st.warning(
            f"No project found with Project ID {update_project_id}."
        )

    else:
        st.session_state["project_to_update"] = project


if "project_to_update" in st.session_state:

    project = st.session_state["project_to_update"]

    st.write("### Edit Project Details")

    col1, col2 = st.columns(2)

    with col1:

        update_project_name = st.text_input(
            "Project Name",
            value=project.project_name,
            key="update_project_name"
        )

        update_department_id = st.number_input(
            "Department ID",
            min_value=1,
            max_value=3,
            value=project.department_id,
            step=1,
            key="update_department_id"
        )

        update_start_date = st.date_input(
            "Start Date",
            value=project.start_date,
            key="update_start_date"
        )

    with col2:

        update_budget = st.number_input(
            "Budget",
            min_value=0.0,
            value=float(project.budget or 0),
            step=1000.0,
            key="update_budget"
        )

        update_status = st.selectbox(
            "Status",
            ["Planned", "Active", "Completed", "On Hold"],
            index=(
                ["Planned", "Active", "Completed", "On Hold"].index(
                    project.status
                )
                if project.status in
                ["Planned", "Active", "Completed", "On Hold"]
                else 0
            ),
            key="update_status"
        )

        update_end_date = st.date_input(
            "End Date",
            value=project.end_date,
            key="update_end_date"
        )

    if st.button(
        "Save Project Changes",
        type="primary",
        key="save_project"
    ):

        if not update_project_name.strip():
            st.error("Project name is required.")

        elif update_end_date < update_start_date:
            st.error("End date cannot be before start date.")

        elif update_budget <= 0:
            st.error("Budget must be greater than 0.")

        else:

            updated_project = Project(
                project_id=project.project_id,
                project_name=update_project_name.strip(),
                department_id=update_department_id,
                start_date=update_start_date,
                end_date=update_end_date,
                budget=update_budget,
                status=update_status
            )

            manager = ProjectManager()

            success = manager.update_project(updated_project)

            if success:

                st.success(
                    f"Project {project.project_id} "
                    "updated successfully."
                )

                st.session_state.pop("project_to_update")

            else:

                st.error(
                    "Project could not be updated."
                )


st.divider()


# ============================================================
# DELETE PROJECT
# ============================================================

st.subheader("Delete Project")

delete_project_id = st.number_input(
    "Project ID to Delete",
    min_value=1,
    step=1,
    value=1,
    key="delete_project_id"
)

if st.button(
    "Delete Project",
    type="primary",
    key="delete_project"
):

    manager = ProjectManager()

    project = manager.get_project(delete_project_id)

    if project is None:

        st.error(
            f"Project {delete_project_id} not found."
        )

    else:

        success = manager.delete_project(delete_project_id)

        if success:

            st.success(
                f"Project {delete_project_id} "
                "deleted successfully."
            )

        else:

            st.error(
                f"Project {delete_project_id} could not be deleted. "
                "It may be referenced by assignments or reviews."
            )


st.divider()


# ============================================================
# VIEW ALL PROJECTS
# ============================================================

st.subheader("All Projects")

if st.button("Load All Projects"):

    manager = ProjectManager()

    projects = manager.get_all_projects()

    if not projects:

        st.info("No projects found.")

    else:

        project_data = []

        for project in projects:

            project_data.append(
                {
                    "Project ID": project.project_id,
                    "Project Name": project.project_name,
                    "Department ID": project.department_id,
                    "Start Date": project.start_date,
                    "End Date": project.end_date,
                    "Budget": project.budget,
                    "Status": project.status
                }
            )

        st.dataframe(
            project_data,
            width="stretch"
        )