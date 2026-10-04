from models.project import Project


project = Project(
    project_id=9999,
    project_name="AI Analytics Platform",
    department_id=2,
    start_date="2026-10-01",
    end_date="2027-03-31",
    budget=250000,
    status="Active"
)

print("Project ID:", project.project_id)
print("Project:", project.project_name)
print("Department ID:", project.department_id)
print("Budget:", project.budget)
print("Status:", project.status)