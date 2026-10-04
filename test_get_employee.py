from managers.employee_manager import EmployeeManager


manager = EmployeeManager()

employee = manager.get_employee("TEST001")

if employee:
    print("Employee found")
    print("ID:", employee.employee_id)
    print("Name:", employee.first_name, employee.last_name)
    print("Email:", employee.email)
    print("Role:", employee.job_role)
else:
    print("Employee not found")