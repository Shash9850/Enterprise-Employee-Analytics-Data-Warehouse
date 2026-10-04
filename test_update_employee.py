from managers.employee_manager import EmployeeManager


manager = EmployeeManager()

employee = manager.get_employee("TEST001")

employee.first_name = "Updated"
employee.last_name = "Employee"
employee.job_role = "Senior Data Scientist"
employee.monthly_income = 7000

result = manager.update_employee(employee)

print("Employee updated:", result)

updated_employee = manager.get_employee("TEST001")

print("Name:", updated_employee.first_name, updated_employee.last_name)
print("Role:", updated_employee.job_role)
print("Salary:", updated_employee.monthly_income)