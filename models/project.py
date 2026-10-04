class Project:
    """Represent a project in the application."""

    def __init__(
        self,
        project_id,
        project_name,
        department_id,
        start_date=None,
        end_date=None,
        budget=None,
        status=None
    ):
        """Initialize a project with the provided details."""
        self.project_id = project_id
        self.project_name = project_name
        self.department_id = department_id
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.status = status