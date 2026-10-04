from managers.project_manager import ProjectManager


manager = ProjectManager()

projects = manager.get_all_projects()

print("Total projects:", len(projects))

print("\nFirst 5 projects:")

for project in projects[:5]:
    print(
        project.project_id,
        "-",
        project.project_name,
        "- Department:",
        project.department_id,
        "- Status:",
        project.status
    )