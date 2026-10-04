from managers.project_manager import ProjectManager


manager = ProjectManager()

project = manager.get_project(8888)

if project:
    print("Project found:")
    print("Project ID:", project.project_id)
    print("Project Name:", project.project_name)
    print("Department ID:", project.department_id)
    print("Budget:", project.budget)
    print("Status:", project.status)
else:
    print("Project not found")