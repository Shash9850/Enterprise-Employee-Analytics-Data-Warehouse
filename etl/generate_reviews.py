import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

EMPLOYEE_FILE = "data/generated/employees_100k.csv"
PROJECT_FILE = "data/generated/projects.csv"
ASSIGNMENT_FILE = "data/generated/employee_projects.csv"

OUTPUT_DIR = Path("data/generated")

NUMBER_OF_REVIEWS = 200_000
SEED = 42


# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------

fake = Faker()
Faker.seed(SEED)
np.random.seed(SEED)


# ------------------------------------------------------------
# Review comments
# ------------------------------------------------------------

POSITIVE_COMMENTS = [
    "Consistently delivers quality work and meets expectations.",
    "Demonstrates strong ownership and good collaboration.",
    "Shows good technical and problem-solving skills.",
    "Communicates effectively and completes assigned tasks on time.",
    "Demonstrates strong performance throughout the review period.",
]

NEUTRAL_COMMENTS = [
    "Meets most expectations and continues to improve.",
    "Performance is consistent with the role requirements.",
    "Shows steady progress and contributes to the team.",
    "Meets expectations with opportunities for further development.",
]

IMPROVEMENT_COMMENTS = [
    "Needs improvement in consistency and task completion.",
    "Would benefit from stronger communication and planning.",
    "Additional support and development may be helpful.",
    "Should focus on improving delivery consistency.",
]


# ------------------------------------------------------------
# Load source data
# ------------------------------------------------------------

def load_data():
    """Load employees, projects, and employee-project assignments."""

    print("Loading employees...")
    employees = pd.read_csv(EMPLOYEE_FILE)

    print("Loading projects...")
    projects = pd.read_csv(PROJECT_FILE)

    print("Loading assignments...")
    assignments = pd.read_csv(ASSIGNMENT_FILE)

    return employees, projects, assignments


# ------------------------------------------------------------
# Prepare valid review assignments
# ------------------------------------------------------------

def prepare_assignments(assignments, employees):
    """Prepare employee-project assignment windows valid for review generation."""

    required_columns = [
        "employee_id",
        "project_id",
        "start_date",
        "end_date"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in assignments.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Assignment data is missing required columns: {missing_columns}"
        )

    assignments = assignments[required_columns].copy()

    assignments["start_date"] = pd.to_datetime(
        assignments["start_date"]
    )

    assignments["end_date"] = pd.to_datetime(
        assignments["end_date"]
    )

    employees_for_lookup = employees[
        ["employee_id", "hire_date"]
    ].copy()

    employees_for_lookup["hire_date"] = pd.to_datetime(
        employees_for_lookup["hire_date"]
    )

    assignments = assignments.merge(
        employees_for_lookup,
        on="employee_id",
        how="left"
    )

    if assignments["hire_date"].isna().any():
        raise ValueError(
            "Some assignments reference employees without a valid hire date."
        )

    # An employee cannot participate in a project before joining the company.
    assignments["valid_start_date"] = assignments[
        ["start_date", "hire_date"]
    ].max(axis=1)

    # Remove assignments that ended before the employee joined.
    assignments = assignments[
        assignments["end_date"] >= assignments["valid_start_date"]
    ].copy()

    # Use the employee's actual employment start as the earliest
    # possible review date.
    assignments["start_date"] = assignments["valid_start_date"]

    assignments = assignments[
        [
            "employee_id",
            "project_id",
            "start_date",
            "end_date"
        ]
    ]

    assignments = assignments.dropna(
        subset=[
            "employee_id",
            "project_id",
            "start_date",
            "end_date"
        ]
    )

    return assignments


# ------------------------------------------------------------
# Generate reviews
# ------------------------------------------------------------

def generate_reviews(assignments, employees, number_of_reviews):
    """Generate realistic performance reviews from valid assignments."""

    print(
        f"\nGenerating {number_of_reviews:,} performance reviews..."
    )

    employee_lookup = employees.set_index("employee_id")

    selected_indices = np.random.randint(
        0,
        len(assignments),
        size=number_of_reviews
    )

    selected_assignments = assignments.iloc[
        selected_indices
    ].reset_index(drop=True)

    reviews = []

    for review_id, assignment in enumerate(
        selected_assignments.itertuples(index=False),
        start=1
    ):
        employee_id = assignment.employee_id
        project_id = int(assignment.project_id)

        review_start_date = assignment.start_date
        end_date = assignment.end_date

        review_date = fake.date_between(
            start_date=review_start_date.date(),
            end_date=end_date.date()
        )

        performance_rating = int(
            np.random.choice(
                [1, 2, 3, 4, 5],
                p=[0.05, 0.10, 0.35, 0.35, 0.15]
            )
        )

        if performance_rating >= 4:
            comments = np.random.choice(
                POSITIVE_COMMENTS
            )
        elif performance_rating == 3:
            comments = np.random.choice(
                NEUTRAL_COMMENTS
            )
        else:
            comments = np.random.choice(
                IMPROVEMENT_COMMENTS
            )

        # Select a reviewer who is different from the employee.
        reviewer_employee_id = np.random.choice(
            employees.loc[
                employees["employee_id"] != employee_id,
                "employee_id"
            ]
        )

        reviewer = employee_lookup.loc[
            reviewer_employee_id
        ]

        reviewer_name = (
            f"{reviewer['first_name']} "
            f"{reviewer['last_name']}"
        )

        reviews.append(
            {
                "review_id": review_id,
                "employee_id": employee_id,
                "project_id": project_id,
                "review_date": review_date,
                "performance_rating": performance_rating,
                "reviewer_name": reviewer_name,
                "comments": comments,
            }
        )

        if review_id % 25_000 == 0:
            print(
                f"Generated {review_id:,} reviews..."
            )

    return pd.DataFrame(reviews)


# ------------------------------------------------------------
# Save reviews
# ------------------------------------------------------------

def save_reviews(df):
    """Save generated performance reviews as a CSV file."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = OUTPUT_DIR / "reviews.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("\n================================")
    print("REVIEW GENERATION COMPLETE")
    print("================================")
    print(f"Output file: {output_file}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    employees, projects, assignments = load_data()

    assignments = prepare_assignments(
        assignments,
        employees
    )

    print(
        f"\nValid review assignment windows: "
        f"{len(assignments):,}"
    )

    reviews = generate_reviews(
        assignments,
        employees,
        NUMBER_OF_REVIEWS
    )

    print("\nFirst 5 reviews:")
    print(
        reviews.head().to_string(index=False)
    )

    print("\nRating distribution:")
    print(
        reviews["performance_rating"]
        .value_counts()
        .sort_index()
    )

    save_reviews(reviews)


if __name__ == "__main__":
    main()