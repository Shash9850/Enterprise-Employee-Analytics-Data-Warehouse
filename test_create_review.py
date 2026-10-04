from managers.review_manager import ReviewManager
from models.review import Review


review = Review(
    review_id=999997,
    employee_id="E000001",
    project_id=1,
    review_date="2026-10-02",
    performance_rating=6,
    reviewer_name="Test Reviewer",
    comments="Testing invalid rating."
)

manager = ReviewManager()

result = manager.create_review(review)

print("Review created:", result)