import streamlit as st
from datetime import date

from managers.employee_manager import EmployeeManager
from models.employee import Employee


st.title("Employee Onboarding")

st.write(
    "Add a new employee to the organization's workforce database."
)

st.divider()

with st.form("employee_onboarding_form"):

    st.subheader("Employee Details")

    col1, col2 = st.columns(2)

    with col1:
        employee_id = st.text_input(
            "Employee ID",
            placeholder="Example: E100001"
        )

        first_name = st.text_input(
            "First Name",
            placeholder="Enter first name"
        )

        last_name = st.text_input(
            "Last Name",
            placeholder="Enter last name"
        )

        email = st.text_input(
            "Email",
            placeholder="employee@company.com"
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=25
        )

    with col2:
        department_id = st.number_input(
            "Department ID",
            min_value=1,
            step=1
        )

        job_role = st.text_input(
            "Job Role",
            placeholder="Example: Data Scientist"
        )

        job_level = st.number_input(
            "Job Level",
            min_value=1,
            max_value=5,
            value=1
        )

        monthly_income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            step=100.0
        )

        hire_date = st.date_input(
            "Hire Date",
            value=date.today()
        )

        attrition = st.selectbox(
            "Attrition",
            ["No", "Yes"]
        )

    submitted = st.form_submit_button(
        "Add Employee",
        type="primary"
    )

if submitted:
    errors = []

    if not employee_id.strip():
        errors.append("Employee ID is required.")

    if not first_name.strip():
        errors.append("First name is required.")

    if not last_name.strip():
        errors.append("Last name is required.")

    if not email.strip():
        errors.append("Email is required.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        errors.append("Please enter a valid email address.")

    if not job_role.strip():
        errors.append("Job role is required.")

    if monthly_income <= 0:
        errors.append("Monthly income must be greater than 0.")

    if errors:
        for error in errors:
            st.error(error)

    else:
        employee = Employee(
            employee_id=employee_id.strip(),
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

        success = manager.create_employee(employee)

        if success:
            st.success(
                f"Employee {employee_id} onboarded successfully."
            )
        else:
            st.error(
                "Employee could not be added. "
                "The Employee ID or email may already exist, "
                "or the department may be invalid."
            )