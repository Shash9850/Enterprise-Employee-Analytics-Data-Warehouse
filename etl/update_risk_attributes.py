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
    "database": os.getenv("MYSQL_DATABASE"),
}


def get_connection():
    """Create a connection to the OLTP database."""
    return mysql.connector.connect(
        host=DATABASE_CONFIG["host"],
        port=DATABASE_CONFIG["port"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        database=DATABASE_CONFIG["database"],
    )


def main():
    """Update employee satisfaction attributes from the generated dataset."""
    employees = pd.read_csv(
        "data/generated/employees_100k.csv",
        usecols=[
            "employee_id",
            "job_satisfaction",
            "environment_satisfaction",
            "work_life_balance",
            "job_involvement",
            "relationship_satisfaction",
        ],
    )

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE employees
        SET
            job_satisfaction = %s,
            environment_satisfaction = %s,
            work_life_balance = %s,
            job_involvement = %s,
            relationship_satisfaction = %s
        WHERE employee_id = %s
    """

    records = [
        (
            row.job_satisfaction,
            row.environment_satisfaction,
            row.work_life_balance,
            row.job_involvement,
            row.relationship_satisfaction,
            row.employee_id,
        )
        for row in employees.itertuples(index=False)
    ]

    try:
        cursor.executemany(query, records)
        connection.commit()
        print(f"Employee risk attributes updated: {cursor.rowcount:,}")

    except Exception as error:
        connection.rollback()
        print(f"Update failed: {error}")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()