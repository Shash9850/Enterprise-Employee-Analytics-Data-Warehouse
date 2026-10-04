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
    "database": os.getenv("MYSQL_DW_DATABASE", "greenfield_dw"),
}


def get_connection():
    """Create and return a connection to the data warehouse."""
    return mysql.connector.connect(**DATABASE_CONFIG)


def load_csv(file_path):
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def prepare_records(dataframe, columns):
    """Convert selected DataFrame columns into database-ready records."""
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


def load_employee_dimension(cursor, connection):
    """
    Load current and historical employee versions into Dim_Employee.

    Employees with SCD Type 2 history are loaded from employee_history.csv.
    Employees without history are loaded from employees_100k.csv.
    """

    print("\nLoading employee dimension...")

    employees = load_csv(
        "data/generated/employees_100k.csv"
    )

    history = load_csv(
        "data/generated/employee_history.csv"
    )

    # ---------------------------------------------------------
    # Safety check: do not accidentally load the dimension twice
    # ---------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM dim_employee"
    )

    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        raise RuntimeError(
            "dim_employee already contains data. "
            "Clear the dimension before running this initial load again."
        )

    # ---------------------------------------------------------
    # Department mapping
    # ---------------------------------------------------------

    department_query = """
        SELECT department_key, department_name
        FROM dim_department
    """

    cursor.execute(department_query)

    department_rows = cursor.fetchall()

    department_mapping = {
        department_name: department_key
        for department_key, department_name in department_rows
    }

    # ---------------------------------------------------------
    # Validate department values
    # ---------------------------------------------------------

    all_departments = set(
        employees["department"].dropna().unique()
    )

    history_departments = set(
        history["department"].dropna().unique()
    )

    unknown_departments = (
        all_departments
        | history_departments
    ) - set(department_mapping)

    if unknown_departments:
        raise ValueError(
            "Unknown department values found: "
            f"{sorted(unknown_departments)}"
        )

    # ---------------------------------------------------------
    # Load SCD Type 2 history records
    # ---------------------------------------------------------

    history_records = history.copy()

    history_records["department_key"] = (
        history_records["department"]
        .map(department_mapping)
    )

    history_records = history_records.rename(
        columns={
            "effective_start_date": "start_date",
            "effective_end_date": "end_date"
        }
    )

    history_columns = [
        "employee_id",
        "first_name",
        "last_name",
        "gender",
        "job_role",
        "job_level",
        "monthly_income",
        "department_key",
        "start_date",
        "end_date",
        "is_current"
    ]

    history_records = prepare_records(
        history_records,
        history_columns
    )

    # ---------------------------------------------------------
    # Find employees that do NOT have SCD Type 2 history
    # ---------------------------------------------------------

    history_employee_ids = set(
        history["employee_id"]
    )

    current_employees = employees[
        ~employees["employee_id"].isin(
            history_employee_ids
        )
    ].copy()

    # ---------------------------------------------------------
    # Prepare normal current employee records
    # ---------------------------------------------------------

    current_employees["department_key"] = (
        current_employees["department"]
        .map(department_mapping)
    )

    current_employees["start_date"] = (
        current_employees["hire_date"]
    )

    current_employees["end_date"] = None

    current_employees["is_current"] = 1

    current_columns = [
        "employee_id",
        "first_name",
        "last_name",
        "gender",
        "job_role",
        "job_level",
        "monthly_income",
        "department_key",
        "start_date",
        "end_date",
        "is_current"
    ]

    current_records = prepare_records(
        current_employees,
        current_columns
    )

    # ---------------------------------------------------------
    # Combine both groups
    # ---------------------------------------------------------

    all_records = (
        history_records
        + current_records
    )

    insert_query = """
        INSERT INTO dim_employee (
            employee_id,
            first_name,
            last_name,
            gender,
            job_role,
            job_level,
            monthly_income,
            department_key,
            start_date,
            end_date,
            is_current
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s
        )
    """

    cursor.executemany(
        insert_query,
        all_records
    )

    connection.commit()

    print(
        f"Historical/current SCD records loaded: "
        f"{len(history_records):,}"
    )

    print(
        f"Employees without history loaded: "
        f"{len(current_records):,}"
    )

    print(
        f"Total Dim_Employee rows loaded: "
        f"{len(all_records):,}"
    )


def main():
    """Run the employee dimension loading process."""

    print("Connecting to MySQL Data Warehouse...")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        load_employee_dimension(
            cursor,
            connection
        )

        print("\n================================")
        print("DIM_EMPLOYEE LOAD COMPLETE")
        print("================================")

    except Exception as error:
        connection.rollback()

        print("\nDim_Employee loading failed.")
        print(f"Error: {error}")

        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()