import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


DATABASE_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}


def get_connection():
    """Create a connection to the OLTP database."""
    return mysql.connector.connect(
        host=DATABASE_CONFIG["host"],
        port=DATABASE_CONFIG["port"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        database=DATABASE_CONFIG["database"]
    )


def main():
    """Update employee tenure values in the OLTP database."""
    employees = pd.read_csv(
        "data/generated/employees_100k.csv",
        usecols=["employee_id", "years_at_company"]
    )

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE employees
        SET years_at_company = %s
        WHERE employee_id = %s
    """

    records = [
        (row.years_at_company, row.employee_id)
        for row in employees.itertuples(index=False)
    ]

    try:
        cursor.executemany(query, records)
        connection.commit()

        print(f"Employee tenure values updated: {cursor.rowcount:,}")

    except Exception as error:
        connection.rollback()
        print(f"Update failed: {error}")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()