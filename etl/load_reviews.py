import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv


REVIEW_FILE = "data/generated/reviews.csv"


def get_connection():
    """Create a connection to the OLTP MySQL database."""

    load_dotenv()

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


def load_reviews(cursor, connection):
    """Load generated performance reviews into the OLTP database."""

    reviews = pd.read_csv(REVIEW_FILE)

    columns = [
        "review_id",
        "employee_id",
        "project_id",
        "review_date",
        "performance_rating",
        "reviewer_name",
        "comments"
    ]

    records = reviews[columns].copy()

    records = records.astype(object)
    records = records.where(
        pd.notna(records),
        None
    )

    records = list(
        records.itertuples(
            index=False,
            name=None
        )
    )

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

    cursor.executemany(
        query,
        records
    )

    connection.commit()

    print(
        f"Reviews loaded: {len(records):,}"
    )


def main():
    """Load the corrected review dataset into the OLTP database."""

    print("Connecting to MySQL OLTP database...")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        print("\nLoading reviews...")

        load_reviews(
            cursor,
            connection
        )

        print("\n================================")
        print("REVIEW LOAD COMPLETE")
        print("================================")

    except Exception as error:
        connection.rollback()

        print("\nReview loading failed.")
        print(f"Error: {error}")

        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()