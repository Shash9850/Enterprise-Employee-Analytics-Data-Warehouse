from managers.employee_manager import EmployeeManager


manager = EmployeeManager()

employees = manager.get_all_employees()

print("Total employees:", len(employees))

print("\nFirst 5 employees:")

for employee in employees[:5]:
    print(
        employee.employee_id,
        "-",
        employee.first_name,
        employee.last_name,
        "-",
        employee.job_role
    )