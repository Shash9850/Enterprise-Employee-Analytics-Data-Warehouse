from managers.db_manager import DatabaseConnection
from models.review import Review
import mysql.connector


class ReviewManager:
    """Handle performance-review database operations."""

    def __init__(self):
        """Initialize the review manager."""
        self.db = DatabaseConnection()

    def get_connection(self):
        """Return an active database connection."""
        return self.db.connect()



    


    def create_review(self, review):
        """Insert a performance review into the OLTP database."""

        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            # Generate the next review ID because review_id
            # is not configured as AUTO_INCREMENT.
            cursor.execute(
                """
                SELECT COALESCE(MAX(review_id), 0) + 1
                FROM reviews
                """
            )

            next_review_id = cursor.fetchone()[0]

            query = """
                INSERT INTO reviews (
                    review_id,
                    employee_id,
                    project_id,
                    review_date,
                    performance_rating,
                    reviewer_name,
                    comments
                )
                VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s
                )
            """

            values = (
                next_review_id,
                review.employee_id,
                review.project_id,
                review.review_date,
                review.performance_rating,
                review.reviewer_name,
                review.comments
            )

            cursor.execute(query, values)
            connection.commit()

            # Store the generated ID in the Review object.
            review.review_id = next_review_id

            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Review could not be created: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()















    def get_review(self, review_id):
        """Retrieve a performance review by review ID."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                review_id,
                employee_id,
                project_id,
                review_date,
                performance_rating,
                reviewer_name,
                comments
            FROM reviews
            WHERE review_id = %s
        """

        try:
            cursor.execute(query, (review_id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return Review(
                review_id=row[0],
                employee_id=row[1],
                project_id=row[2],
                review_date=row[3],
                performance_rating=row[4],
                reviewer_name=row[5],
                comments=row[6]
            )

        finally:
            cursor.close()










    def get_all_reviews(self):
        """Retrieve all performance reviews from the OLTP database."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                review_id,
                employee_id,
                project_id,
                review_date,
                performance_rating,
                reviewer_name,
                comments
            FROM reviews
            ORDER BY review_id
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            reviews = []

            for row in rows:
                review = Review(
                    review_id=row[0],
                    employee_id=row[1],
                    project_id=row[2],
                    review_date=row[3],
                    performance_rating=row[4],
                    reviewer_name=row[5],
                    comments=row[6]
                )

                reviews.append(review)

            return reviews

        finally:
            cursor.close()













    def update_review(self, review):
        """Update an existing performance review."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE reviews
            SET
                employee_id = %s,
                project_id = %s,
                review_date = %s,
                performance_rating = %s,
                reviewer_name = %s,
                comments = %s
            WHERE review_id = %s
        """

        values = (
            review.employee_id,
            review.project_id,
            review.review_date,
            review.performance_rating,
            review.reviewer_name,
            review.comments,
            review.review_id
        )

        try:
            cursor.execute(query, values)

            if cursor.rowcount == 0:
                return False

            connection.commit()
            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Review could not be updated: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()














    def delete_review(self, review_id):
        """Delete a performance review by review ID."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM reviews
            WHERE review_id = %s
        """

        try:
            cursor.execute(query, (review_id,))

            if cursor.rowcount == 0:
                return False

            connection.commit()
            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Review could not be deleted: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()