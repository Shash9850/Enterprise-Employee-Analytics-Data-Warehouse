


class Employee:
    """Represent an employee in the application."""

    def __init__(
        self,
        employee_id,
        first_name,
        last_name,
        email,
        gender=None,
        age=None,
        department_id=None,
        job_role=None,
        job_level=None,
        monthly_income=None,
        hire_date=None,
        attrition=None
    ):
        """Initialize an employee with the provided details."""
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.age = age
        self.department_id = department_id
        self.job_role = job_role
        self.job_level = job_level
        self.monthly_income = monthly_income
        self.hire_date = hire_date
        self.attrition = attrition