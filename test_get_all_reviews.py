from managers.review_manager import ReviewManager


manager = ReviewManager()

reviews = manager.get_all_reviews()

print("Total reviews:", len(reviews))

print("\nFirst 5 reviews:")

for review in reviews[:5]:
    print(
        review.review_id,
        "- Employee:",
        review.employee_id,
        "- Project:",
        review.project_id,
        "- Rating:",
        review.performance_rating
    )












    