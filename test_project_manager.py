from managers.project_manager import ProjectManager


manager = ProjectManager()

connection = manager.get_connection()

print("Project manager connected:", connection.is_connected())
print("Database:", connection.database)