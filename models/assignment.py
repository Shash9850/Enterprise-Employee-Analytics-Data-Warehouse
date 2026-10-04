class Assignment:
    """Represent an employee-to-project assignment."""

    def __init__(
        self,
        assignment_id=None,
        employee_id=None,
        project_id=None,
        allocation_percent=None,
        start_date=None,
        end_date=None,
    ):
        self.assignment_id = assignment_id
        self.employee_id = employee_id
        self.project_id = project_id
        self.allocation_percent = allocation_percent
        self.start_date = start_date
        self.end_date = end_date