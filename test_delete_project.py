from managers.project_manager import ProjectManager


manager = ProjectManager()

result = manager.delete_project(1)

print("Project deleted:", result)

project = manager.get_project(1)

if project is None:
    print("Project no longer exists")
else:
    print("Project still exists")