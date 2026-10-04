from models.employee import Employee


employee = Employee(
    employee_id="E000001",
    first_name="John",
    last_name="Smith",
    email="john.smith@example.com",
    department_id=2,
    job_role="Data Scientist",
    job_level=2,
    monthly_income=7500
)

print("Employee ID:", employee.employee_id)
print("Name:", employee.first_name, employee.last_name)
print("Role:", employee.job_role)
print("Department ID:", employee.department_id)