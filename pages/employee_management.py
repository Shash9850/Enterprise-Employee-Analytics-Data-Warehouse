import streamlit as st

from managers.employee_manager import EmployeeManager
from managers.scd2_manager import SCD2Manager
from models.employee import Employee


st.title("Employee Management")

st.write(
    "Search and view employee information from the workforce database."
)

st.divider()

st.subheader("Find Employee")

employee_id = st.text_input(
    "Employee ID",
    placeholder="Example: E999999"
)

if st.button("Search Employee", type="primary"):

    if not employee_id.strip():
        st.error("Employee ID is required.")

    else:
        manager = EmployeeManager()
        employee = manager.get_employee(employee_id.strip())

        if employee is None:
            st.warning("No employee found with this Employee ID.")

        else:
            st.success("Employee found.")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Employee ID:**", employee.employee_id)
                st.write("**First Name:**", employee.first_name)
                st.write("**Last Name:**", employee.last_name)
                st.write("**Email:**", employee.email)
                st.write("**Gender:**", employee.gender)
                st.write("**Age:**", employee.age)

            with col2:
                st.write("**Department ID:**", employee.department_id)
                st.write("**Job Role:**", employee.job_role)
                st.write("**Job Level:**", employee.job_level)
                st.write("**Monthly Income:**", employee.monthly_income)
                st.write("**Hire Date:**", employee.hire_date)
                st.write("**Attrition:**", employee.attrition)








st.divider()

st.subheader("Update Employee")

update_employee_id = st.text_input(
    "Employee ID to Update",
    placeholder="Example: E999999",
    key="update_employee_id"
)

if st.button("Load Employee", key="load_employee"):

    if not update_employee_id.strip():
        st.error("Employee ID is required.")

    else:
        manager = EmployeeManager()
        employee = manager.get_employee(update_employee_id.strip())

        if employee is None:
            st.warning("No employee found with this Employee ID.")

        else:
            st.session_state["employee_to_update"] = employee


if "employee_to_update" in st.session_state:

    employee = st.session_state["employee_to_update"]

    st.write("### Edit Employee Details")

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input(
            "First Name",
            value=employee.first_name,
            key="update_first_name"
        )

        last_name = st.text_input(
            "Last Name",
            value=employee.last_name,
            key="update_last_name"
        )

        email = st.text_input(
            "Email",
            value=employee.email,
            key="update_email"
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"],
            index=["Male", "Female"].index(employee.gender)
            if employee.gender in ["Male", "Female"]
            else 0,
            key="update_gender"
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=70,
            value=employee.age or 18,
            step=1,
            key="update_age"
        )

    with col2:
        job_role = st.text_input(
            "Job Role",
            value=employee.job_role or "",
            key="update_job_role"
        )
        department_id = st.number_input(
            "Department ID",
            min_value=1,
            step=1,
            value=employee.department_id,
            key="update_department_id"
        )

        job_level = st.number_input(
            "Job Level",
            min_value=1,
            max_value=5,
            value=employee.job_level or 1,
            step=1,
            key="update_job_level"
        )

        monthly_income = st.number_input(
            "Monthly Income",
            min_value=0.01,
            value=float(employee.monthly_income or 0),
            step=100.0,
            key="update_income"
        )

        hire_date = st.date_input(
            "Hire Date",
            value=employee.hire_date,
            key="update_hire_date"
        )

        attrition = st.selectbox(
            "Attrition",
            ["Yes", "No"],
            index=["Yes", "No"].index(employee.attrition)
            if employee.attrition in ["Yes", "No"]
            else 1,
            key="update_attrition"
        )

        if st.button("Save Changes", type="primary", key="save_employee"):

            if not first_name.strip():
                st.error("First name is required.")

            elif not last_name.strip():
                st.error("Last name is required.")

            elif not email.strip():
                st.error("Email is required.")

            elif not job_role.strip():
                st.error("Job role is required.")

            elif monthly_income <= 0:
                st.error("Monthly income must be greater than 0.")

            else:
                department_changed = (
                    employee.department_id != department_id
                )

                updated_employee = Employee(
                    employee_id=employee.employee_id,
                    first_name=first_name.strip(),
                    last_name=last_name.strip(),
                    email=email.strip(),
                    gender=gender,
                    age=age,
                    department_id=department_id,
                    job_role=job_role.strip(),
                    job_level=job_level,
                    monthly_income=monthly_income,
                    hire_date=hire_date,
                    attrition=attrition
                )

                manager = EmployeeManager()

                success = manager.update_employee(updated_employee)

                if success:

                    # Run SCD Type 2 only when the department changes.
                    if department_changed:
                        scd2_manager = SCD2Manager()

                        scd2_success = scd2_manager.update_employee_department(
                            employee.employee_id,
                            department_id
                        )

                        if scd2_success:
                            st.success(
                                f"Employee {employee.employee_id} updated "
                                "successfully with SCD Type 2 history."
                            )
                        else:
                            st.warning(
                                f"Employee {employee.employee_id} was updated, "
                                "but the SCD Type 2 history could not be updated."
                            )

                    else:
                        st.success(
                            f"Employee {employee.employee_id} updated successfully."
                        )

                    st.session_state.pop("employee_to_update")

                else:
                    st.error(
                        "Employee could not be updated. "
                        "The email may already exist or a database error occurred."
                    )












st.divider()

st.subheader("Delete Employee")

delete_employee_id = st.text_input(
    "Employee ID",
    placeholder="e.g. E999999",
    key="delete_employee_id"
)

if st.button("Delete Employee", type="primary", key="delete_employee"):
    if not delete_employee_id.strip():
        st.warning("Please enter an Employee ID.")
    else:
        manager = EmployeeManager()

        employee = manager.get_employee(delete_employee_id.strip())

        if employee is None:
            st.error(f"Employee {delete_employee_id.strip()} not found.")
        else:
            success = manager.delete_employee(delete_employee_id.strip())

            if success:
                st.success(
                    f"Employee {delete_employee_id.strip()} deleted successfully."
                )
            else:
                st.error(
                    f"Employee {delete_employee_id.strip()} could not be deleted."
                )