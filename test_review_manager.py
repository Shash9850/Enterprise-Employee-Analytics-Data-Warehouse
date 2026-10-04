from managers.review_manager import ReviewManager


manager = ReviewManager()

connection = manager.get_connection()

print("Review manager connected:", connection.is_connected())
print("Database:", connection.database)