import os
from datetime import timedelta

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


def get_review_date_range(cursor):
    """Get the earliest and latest review dates from the OLTP database."""

    query = """
        SELECT
            MIN(review_date),
            MAX(review_date)
        FROM greenfield_oltp.reviews;
    """

    cursor.execute(query)

    min_date, max_date = cursor.fetchone()

    if min_date is None or max_date is None:
        raise ValueError(
            "No review dates were found in the OLTP reviews table."
        )

    return min_date, max_date


def generate_date_records(min_date, max_date):
    """Generate one date-dimension record for every date in the range."""

    records = []

    current_date = min_date

    while current_date <= max_date:

        date_key = int(current_date.strftime("%Y%m%d"))

        record = (
            date_key,
            current_date,
            current_date.day,
            current_date.month,
            current_date.strftime("%B"),
            ((current_date.month - 1) // 3) + 1,
            current_date.year,
        )

        records.append(record)

        current_date += timedelta(days=1)

    return records


def load_date_dimension(cursor, connection):
    """Populate the Dim_Date table."""

    print("\nLoading date dimension...")

    cursor.execute(
        "SELECT COUNT(*) FROM dim_date"
    )

    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        raise RuntimeError(
            "dim_date already contains data. "
            "Clear the dimension before running the initial load again."
        )

    min_date, max_date = get_review_date_range(cursor)

    print(f"Earliest review date: {min_date}")
    print(f"Latest review date:   {max_date}")

    records = generate_date_records(
        min_date,
        max_date
    )

    insert_query = """
        INSERT INTO dim_date (
            date_key,
            full_date,
            day,
            month,
            month_name,
            quarter,
            year
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s
        )
    """

    cursor.executemany(
        insert_query,
        records
    )

    connection.commit()

    print(
        f"Dates loaded: {len(records):,}"
    )


def main():
    """Run the date dimension loading process."""

    print("Connecting to MySQL Data Warehouse...")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        load_date_dimension(
            cursor,
            connection
        )

        print("\n================================")
        print("DIM_DATE LOAD COMPLETE")
        print("================================")

    except Exception as error:
        connection.rollback()

        print("\nDim_Date loading failed.")
        print(f"Error: {error}")

        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()