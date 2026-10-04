from managers.project_manager import ProjectManager
from models.project import Project


project = Project(
    project_id=9999,
    project_name="AI Analytics Platform",
    department_id=99,
    start_date="2026-10-01",
    end_date="2027-06-30",
    budget=300000,
    status="Completed"
)

manager = ProjectManager()

result = manager.update_project(project)

print("Project updated:", result)

updated_project = manager.get_project(9999)

if updated_project:
    print("Project Name:", updated_project.project_name)
    print("End Date:", updated_project.end_date)
    print("Budget:", updated_project.budget)
    print("Status:", updated_project.status)