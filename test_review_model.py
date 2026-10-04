from models.review import Review


review = Review(
    review_id=999999,
    employee_id="E000001",
    project_id=1,
    review_date="2026-10-02",
    performance_rating=5,
    reviewer_name="Test Reviewer",
    comments="Excellent performance."
)

print("Review ID:", review.review_id)
print("Employee ID:", review.employee_id)
print("Project ID:", review.project_id)
print("Rating:", review.performance_rating)
print("Reviewer:", review.reviewer_name)
print("Comments:", review.comments)