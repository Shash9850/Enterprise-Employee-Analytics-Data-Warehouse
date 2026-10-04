from managers.review_manager import ReviewManager


manager = ReviewManager()

result = manager.delete_review(999999)

print("Review deleted:", result)

review = manager.get_review(999999)

if review is None:
    print("Review no longer exists")
else:
    print("Review still exists")