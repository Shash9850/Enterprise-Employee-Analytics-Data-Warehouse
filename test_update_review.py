from managers.review_manager import ReviewManager
from models.review import Review


review = Review(
    review_id=999999,
    employee_id="E000001",
    project_id=1,
    review_date="2026-10-02",
    performance_rating=4,
    reviewer_name="Updated Reviewer",
    comments="Performance improved significantly."
)

manager = ReviewManager()

result = manager.update_review(review)

print("Review updated:", result)

updated_review = manager.get_review(999999)

if updated_review:
    print("Rating:", updated_review.performance_rating)
    print("Reviewer:", updated_review.reviewer_name)
    print("Comments:", updated_review.comments)