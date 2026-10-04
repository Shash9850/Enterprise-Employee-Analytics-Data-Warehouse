import pandas as pd
import numpy as np


INPUT_FILE = "data/generated/employees_100k.csv"
OUTPUT_FILE = "data/generated/employee_history.csv"

HISTORY_EMPLOYEE_PERCENTAGE = 10


def load_employees():
    """Load the generated employee dataset."""

    return pd.read_csv(INPUT_FILE)


def generate_history(employees):
    """Generate SCD Type 2 history for a subset of employees."""

    history_employees = employees.sample(
        frac=HISTORY_EMPLOYEE_PERCENTAGE / 100,
        random_state=42
    ).copy()

    history_records = []

    for _, employee in history_employees.iterrows():

        hire_date = pd.to_datetime(employee["hire_date"])

        # Skip employees who do not have enough employment history.
        if hire_date >= pd.Timestamp("2024-01-01"):
            continue

        change_date = hire_date + pd.Timedelta(
            days=np.random.randint(365, 900)
        )

        # Skip unrealistic change dates.
        if change_date >= pd.Timestamp("2026-01-01"):
            continue

        original_department = employee["department"]
        original_job_level = employee["job_level"]
        original_income = employee["monthly_income"]

        # Select the type of employee change.
        change_type = np.random.choice([
            "department_change",
            "promotion",
            "salary_increase"
        ])

        new_department = original_department
        new_job_level = original_job_level
        new_income = original_income

        # Apply the selected change.
        if change_type == "department_change":

            departments = [
                "Sales",
               "Human Resources",
"Research & Development"
            ]

            available_departments = [
                department
                for department in departments
                if department != original_department
            ]

            new_department = np.random.choice(
                available_departments
            )

        elif change_type == "promotion":

            new_job_level = min(
                original_job_level + 1,
                5
            )

            new_income = round(
                original_income * np.random.uniform(1.08, 1.20),
                2
            )

        elif change_type == "salary_increase":

            new_income = round(
                original_income * np.random.uniform(1.05, 1.15),
                2
            )

        # ---------------------------------------------------------
        # VERSION 1 — HISTORICAL RECORD
        # ---------------------------------------------------------

        history_records.append({
            "employee_id": employee["employee_id"],
            "first_name": employee["first_name"],
            "last_name": employee["last_name"],
            "gender": employee["gender"],
            "department": original_department,
            "job_role": employee["job_role"],
            "job_level": original_job_level,
            "monthly_income": original_income,
            "effective_start_date": hire_date.date(),
            "effective_end_date": (
                change_date - pd.Timedelta(days=1)
            ).date(),
            "is_current": 0,
            "change_type": "Initial"
        })

        # ---------------------------------------------------------
        # VERSION 2 — CURRENT RECORD
        # ---------------------------------------------------------

        history_records.append({
            "employee_id": employee["employee_id"],
            "first_name": employee["first_name"],
            "last_name": employee["last_name"],
            "gender": employee["gender"],
            "department": new_department,
            "job_role": employee["job_role"],
            "job_level": new_job_level,
            "monthly_income": new_income,
            "effective_start_date": change_date.date(),
            "effective_end_date": None,
            "is_current": 1,
            "change_type": change_type
        })

    return pd.DataFrame(history_records)


def main():
    """Generate the employee SCD Type 2 history dataset."""

    print("Loading employees...")

    employees = load_employees()

    print(f"Employees loaded: {len(employees):,}")

    print("\nGenerating SCD Type 2 history...")

    history = generate_history(employees)

    history.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n================================")
    print("SCD HISTORY GENERATION COMPLETE")
    print("================================")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Rows: {len(history):,}")
    print(
        f"Employees with history: "
        f"{history['employee_id'].nunique():,}"
    )

    print("\nVersion distribution:")
    print(
        history["is_current"]
        .value_counts()
        .rename({
            0: "Historical versions",
            1: "Current versions"
        })
    )

    print("\nChange type distribution:")
    print(history["change_type"].value_counts())

    print("\nFirst 10 records:")
    print(history.head(10).to_string(index=False))


if __name__ == "__main__":
    main()