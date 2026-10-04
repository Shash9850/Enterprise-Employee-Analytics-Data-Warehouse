from managers.employee_manager import EmployeeManager


manager = EmployeeManager()

connection = manager.get_connection()

print("Employee manager connected:", connection.is_connected())
print("Database:", connection.database)