from managers.project_manager import ProjectManager
from models.project import Project


project = Project(
    project_id=9998,
    project_name="AI Analytics Platform",
    department_id=999,
    start_date="2026-10-01",
    end_date="2027-03-31",
    budget=250000,
    status="Active"
)

manager = ProjectManager()

result = manager.create_project(project)

print("Project created:", result)