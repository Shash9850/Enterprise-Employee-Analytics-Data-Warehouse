import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


DATABASE_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DW_DATABASE", "greenfield_dw"),
}


def get_connection():
    """Create and return a connection to the data warehouse."""
    return mysql.connector.connect(**DATABASE_CONFIG)


def validate_source_data(cursor):
    """Validate that the required OLTP review data exists."""

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM greenfield_oltp.reviews
        """
    )

    review_count = cursor.fetchone()[0]

    if review_count == 0:
        raise ValueError(
            "No performance reviews were found in the OLTP database."
        )

    return review_count


def load_fact_reviews(cursor, connection):
    """
    Load performance review events into the fact table.

    The employee dimension is joined using the SCD Type 2
    effective date range so each review points to the
    employee version that was valid when the review occurred.
    """

    print("\nLoading Fact_PerformanceReviews...")

    # ---------------------------------------------------------
    # Safety check
    # ---------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM fact_performance_reviews
        """
    )

    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        raise RuntimeError(
            "fact_performance_reviews already contains data. "
            "Clear the fact table before running the initial load again."
        )

    # ---------------------------------------------------------
    # Validate source
    # ---------------------------------------------------------

    review_count = validate_source_data(cursor)

    print(
        f"Source reviews available: {review_count:,}"
    )

    # ---------------------------------------------------------
    # Insert fact records
    # ---------------------------------------------------------

    insert_query = """
        INSERT INTO fact_performance_reviews (
            review_id,
            employee_key,
            project_key,
            date_key,
            department_key,
            performance_rating,
            review_count
        )
        SELECT
            r.review_id,

            e.employee_key,

            p.project_key,

            d.date_key,

            e.department_key,

            r.performance_rating,

            1

        FROM greenfield_oltp.reviews r

        INNER JOIN greenfield_dw.dim_employee e
            ON r.employee_id = e.employee_id
            AND r.review_date >= e.start_date
            AND (
                e.end_date IS NULL
                OR r.review_date <= e.end_date
            )

        LEFT JOIN greenfield_dw.dim_project p
            ON r.project_id = p.project_id

        INNER JOIN greenfield_dw.dim_date d
            ON r.review_date = d.full_date
    """

    cursor.execute(insert_query)

    connection.commit()

    print(
        f"Fact records loaded: {cursor.rowcount:,}"
    )


def main():
    """Run the performance review fact loading process."""

    print("Connecting to MySQL Data Warehouse...")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        load_fact_reviews(
            cursor,
            connection
        )

        print("\n================================")
        print("FACT LOAD COMPLETE")
        print("================================")

    except Exception as error:
        connection.rollback()

        print("\nFact loading failed.")
        print(f"Error: {error}")

        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()