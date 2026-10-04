from managers.employee_manager import EmployeeManager


manager = EmployeeManager()

result = manager.delete_employee("TEST001")

print("Employee deleted:", result)

employee = manager.get_employee("TEST001")

if employee is None:
    print("Employee no longer exists")
else:
    print("Employee still exists")