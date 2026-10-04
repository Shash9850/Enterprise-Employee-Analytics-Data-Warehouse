class Review:
    """Represent a performance review in the application."""

    def __init__(
        self,
        review_id,
        employee_id,
        project_id=None,
        review_date=None,
        performance_rating=None,
        reviewer_name=None,
        comments=None
    ):
        """Initialize a performance review with the provided details."""
        self.review_id = review_id
        self.employee_id = employee_id
        self.project_id = project_id
        self.review_date = review_date
        self.performance_rating = performance_rating
        self.reviewer_name = reviewer_name
        self.comments = comments