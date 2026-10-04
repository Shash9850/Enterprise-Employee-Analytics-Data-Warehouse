import pandas as pd
from pathlib import Path
import numpy as np
from faker import Faker


# -----------------------------
# Configuration
# -----------------------------

EMPLOYEE_FILE = "data/generated/employees_100k.csv"

OUTPUT_DIR = Path("data/generated")


# -----------------------------
# Generate departments
# -----------------------------

def generate_departments():

    departments = [
        {
            "department_id": 1,
            "department_name": "Sales"
        },
        {
            "department_id": 2,
            "department_name": "Research & Development"
        },
        {
            "department_id": 3,
            "department_name": "Human Resources"
        }
    ]

    df = pd.DataFrame(departments)

    output_file = OUTPUT_DIR / "departments.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("Departments created:")
    print(df)

    print(f"\nSaved to: {output_file}")


# -----------------------------
# Generate projects
# -----------------------------

def generate_projects(number_of_projects=500):

    fake = Faker()
    np.random.seed(42)

    departments = {
        1: "Sales",
        2: "Research & Development",
        3: "Human Resources"
    }

    projects = []

    for project_id in range(1, number_of_projects + 1):

        department_id = np.random.choice(
            list(departments.keys())
        )

        start_date = fake.date_between(
            start_date="-5y",
            end_date="-1m"
        )

        end_date = fake.date_between(
            start_date=start_date,
            end_date="+1y"
        )

        budget = int(
            np.random.randint(
                50_000,
                2_000_000
            )
        )

        status = np.random.choice(
            [
                "Planned",
                "Active",
                "Completed"
            ]
        )

        projects.append({
            "project_id": project_id,
            "project_name": f"{fake.bs().title()} Project",
            "department_id": department_id,
            "start_date": start_date,
            "end_date": end_date,
            "budget": budget,
            "status": status
        })

    df = pd.DataFrame(projects)

    output_file = OUTPUT_DIR / "projects.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("\nProjects created:")
    print(df.head())

    print(f"\nTotal projects: {len(df)}")
    print(f"Saved to: {output_file}")


# -----------------------------
# Generate employee-project assignments
# -----------------------------

def generate_assignments(number_of_assignments=200000):

    np.random.seed(42)

    employees = pd.read_csv(EMPLOYEE_FILE)

    projects = pd.read_csv(
        OUTPUT_DIR / "projects.csv"
    )

    # Random employee IDs
    employee_ids = np.random.choice(
        employees["employee_id"].values,
        size=number_of_assignments
    )

    # Random project IDs
    project_ids = np.random.choice(
        projects["project_id"].values,
        size=number_of_assignments
    )

    # Random allocation
    allocation_percent = np.random.choice(
        [25, 50, 75, 100],
        size=number_of_assignments
    )

    # Create assignments
    df = pd.DataFrame({
        "assignment_id": np.arange(
            1,
            number_of_assignments + 1
        ),
        "employee_id": employee_ids,
        "project_id": project_ids,
        "allocation_percent": allocation_percent
    })

    # Add project dates
    df = df.merge(
        projects[
            [
                "project_id",
                "start_date",
                "end_date"
            ]
        ],
        on="project_id",
        how="left"
    )

    # Save
    output_file = OUTPUT_DIR / "employee_projects.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("\nEmployee-project assignments created:")
    print(df.head())

    print(f"\nTotal assignments: {len(df)}")
    print(f"Saved to: {output_file}")


# -----------------------------
# Main
# -----------------------------

def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    generate_departments()
    generate_projects(500)
    generate_assignments(200000)




if __name__ == "__main__":
    main()
