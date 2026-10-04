from managers.employee_manager import EmployeeManager
from models.employee import Employee


employee = Employee(
    employee_id="TEST001",
    first_name="Test",
    last_name="Employee",
    email="test.employee@example.com",
    gender="Male",
    age=25,
    department_id=2,
    job_role="Data Scientist",
    job_level=1,
    monthly_income=6000,
    hire_date="2026-10-02",
    attrition="No"
)

manager = EmployeeManager()

result = manager.create_employee(employee)

print("Employee created:", result)