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
    """Create and return a connection to the OLTP database."""

    return mysql.connector.connect(
        host=DATABASE_CONFIG["host"],
        port=DATABASE_CONFIG["port"],
        user=DATABASE_CONFIG["user"],
        password=DATABASE_CONFIG["password"],
        database=DATABASE_CONFIG["database"]
    )


def load_csv(file_path):
    """Load a CSV file into a pandas DataFrame."""

    return pd.read_csv(file_path)


def prepare_records(dataframe, columns):
    """Convert DataFrame values into MySQL-compatible records."""

    selected_data = dataframe[columns].copy()

    selected_data = selected_data.astype(object)

    selected_data = selected_data.where(
        pd.notna(selected_data),
        None
    )

    return list(
        selected_data.itertuples(
            index=False,
            name=None
        )
    )


def load_departments(cursor, connection):
    """Load department records into the departments table."""

    departments = load_csv(
        "data/generated/departments.csv"
    )

    columns = [
        "department_id",
        "department_name"
    ]

    records = prepare_records(
        departments,
        columns
    )

    query = """
        INSERT INTO departments (
            department_id,
            department_name
        )
        VALUES (%s, %s)
    """

    cursor.executemany(query, records)
    connection.commit()

    print(f"Departments loaded: {len(records):,}")


def load_employees(cursor, connection):
    """Load employee records into the employees table."""

    employees = load_csv(
        "data/generated/employees_100k.csv"
    )

    department_mapping = {
        "Sales": 1,
        "Research & Development": 2,
        "Human Resources": 3
    }

    employees["department_id"] = employees["department"].map(
        department_mapping
    )

    unmapped_departments = employees.loc[
        employees["department_id"].isna(),
        "department"
    ].unique()

    if len(unmapped_departments) > 0:
        raise ValueError(
            "Unmapped department values found: "
            f"{list(unmapped_departments)}"
        )

    columns = [
        "employee_id",
        "first_name",
        "last_name",
        "email",
        "gender",
        "age",
        "department_id",
        "job_role",
        "job_level",
        "monthly_income",
        "hire_date",
        "attrition"
    ]

    records = prepare_records(
        employees,
        columns
    )

    query = """
        INSERT INTO employees (
            employee_id,
            first_name,
            last_name,
            email,
            gender,
            age,
            department_id,
            job_role,
            job_level,
            monthly_income,
            hire_date,
            attrition
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
    """

    cursor.executemany(query, records)
    connection.commit()

    print(f"Employees loaded: {len(records):,}")


def load_projects(cursor, connection):
    """Load project records into the projects table."""

    projects = load_csv(
        "data/generated/projects.csv"
    )

    columns = [
        "project_id",
        "project_name",
        "department_id",
        "start_date",
        "end_date",
        "budget",
        "status"
    ]

    records = prepare_records(
        projects,
        columns
    )

    query = """
        INSERT INTO projects (
            project_id,
            project_name,
            department_id,
            start_date,
            end_date,
            budget,
            status
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s
        )
    """

    cursor.executemany(query, records)
    connection.commit()

    print(f"Projects loaded: {len(records):,}")


def load_assignments(cursor, connection):
    """Load employee-project assignment records."""

    assignments = load_csv(
        "data/generated/employee_projects.csv"
    )

    columns = [
        "assignment_id",
        "employee_id",
        "project_id",
        "allocation_percent",
        "start_date",
        "end_date"
    ]

    records = prepare_records(
        assignments,
        columns
    )

    query = """
        INSERT INTO assignments (
            assignment_id,
            employee_id,
            project_id,
            allocation_percent,
            start_date,
            end_date
        )
        VALUES (
            %s, %s, %s,
            %s, %s, %s
        )
    """

    cursor.executemany(query, records)
    connection.commit()

    print(f"Assignments loaded: {len(records):,}")


def load_reviews(cursor, connection):
    """Load performance review records."""

    reviews = load_csv(
        "data/generated/reviews.csv"
    )

    columns = [
        "review_id",
        "employee_id",
        "project_id",
        "review_date",
        "performance_rating",
        "reviewer_name",
        "comments"
    ]

    records = prepare_records(
        reviews,
        columns
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
            %s, %s, %s,
            %s, %s, %s, %s
        )
    """

    cursor.executemany(query, records)
    connection.commit()

    print(f"Reviews loaded: {len(records):,}")


def main():
    """Run the complete OLTP loading pipeline."""

    print("Connecting to MySQL...")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        print("\nLoading departments...")
        load_departments(cursor, connection)

        print("\nLoading employees...")
        load_employees(cursor, connection)

        print("\nLoading projects...")
        load_projects(cursor, connection)

        print("\nLoading assignments...")
        load_assignments(cursor, connection)

        print("\nLoading reviews...")
        load_reviews(cursor, connection)

        print("\n================================")
        print("OLTP LOAD COMPLETE")
        print("================================")

    except Exception as error:
        connection.rollback()

        print("\nOLTP loading failed.")
        print(f"Error: {error}")

        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()