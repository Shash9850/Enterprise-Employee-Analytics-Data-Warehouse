from managers.review_manager import ReviewManager


manager = ReviewManager()

review = manager.get_review(888888)

if review:
    print("Review found:")
    print("Review ID:", review.review_id)
    print("Employee ID:", review.employee_id)
    print("Project ID:", review.project_id)
    print("Rating:", review.performance_rating)
    print("Reviewer:", review.reviewer_name)
    print("Comments:", review.comments)
else:
    print("Review not found")