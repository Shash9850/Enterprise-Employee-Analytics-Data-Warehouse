import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT_FILE = "data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv"

OUTPUT_DIR = Path("data/generated")

NUM_EMPLOYEES = 100_000

SEED = 42

fake = Faker()
Faker.seed(SEED)
np.random.seed(SEED)


# --------------------------------------------------
# LOAD IBM DATASET
# --------------------------------------------------

def load_source_data():
    print("Loading IBM HR dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Source rows: {len(df):,}")
    print(f"Source columns: {len(df.columns)}")

    return df


# --------------------------------------------------
# GENERATE EMPLOYEES
# --------------------------------------------------

def generate_employees(source_df, number_of_records):

    print(f"\nGenerating {number_of_records:,} employees...")

    records = []

    for i in range(number_of_records):

        # Select a random IBM employee
        source = source_df.iloc[
            np.random.randint(0, len(source_df))
        ]

        # Generate synthetic identity
        first_name = fake.first_name()
        last_name = fake.last_name()

        employee_id = f"E{i + 1:06d}"

        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}."
            f"{i + 1}@company.com"
        )

        # Slightly perturb the original IBM values
        age = max(
            18,
            min(
                65,
                int(
                    source["Age"]
                    + np.random.randint(-3, 4)
                )
            )
        )

        monthly_income = max(
            2000,
            int(
                source["MonthlyIncome"]
                * np.random.uniform(0.85, 1.20)
            )
        )

        daily_rate = max(
            100,
            int(
                source["DailyRate"]
                * np.random.uniform(0.90, 1.10)
            )
        )

        hourly_rate = max(
            20,
            int(
                source["HourlyRate"]
                * np.random.uniform(0.90, 1.10)
            )
        )

        # Synthetic hire date
        hire_date = fake.date_between(
            start_date="-15y",
            end_date="-1y"
        )

        record = {
            "employee_id": employee_id,

            "first_name": first_name,
            "last_name": last_name,
            "email": email,

            "gender": source["Gender"],
            "age": age,

            "department": source["Department"],
            "job_role": source["JobRole"],
            "education_field": source["EducationField"],

            "job_level": source["JobLevel"],

            "monthly_income": monthly_income,
            "daily_rate": daily_rate,
            "hourly_rate": hourly_rate,

            "business_travel": source["BusinessTravel"],

            "distance_from_home": source["DistanceFromHome"],

            "job_involvement": source["JobInvolvement"],
            "job_satisfaction": source["JobSatisfaction"],

            "environment_satisfaction": (
                source["EnvironmentSatisfaction"]
            ),

            "relationship_satisfaction": (
                source["RelationshipSatisfaction"]
            ),

            "performance_rating": (
                source["PerformanceRating"]
            ),

            "percent_salary_hike": (
                source["PercentSalaryHike"]
            ),

            "overtime": source["OverTime"],

            "marital_status": source["MaritalStatus"],

            "stock_option_level": (
                source["StockOptionLevel"]
            ),

            "total_working_years": (
                source["TotalWorkingYears"]
            ),

            "years_at_company": (
                source["YearsAtCompany"]
            ),

            "years_in_current_role": (
                source["YearsInCurrentRole"]
            ),

            "years_since_last_promotion": (
                source["YearsSinceLastPromotion"]
            ),

            "years_with_current_manager": (
                source["YearsWithCurrManager"]
            ),

            "training_times_last_year": (
                source["TrainingTimesLastYear"]
            ),

            "work_life_balance": (
                source["WorkLifeBalance"]
            ),

            "num_companies_worked": (
                source["NumCompaniesWorked"]
            ),

            "attrition": source["Attrition"],

            "hire_date": hire_date,
        }

        records.append(record)

        # Progress indicator
        if (i + 1) % 10_000 == 0:
            print(
                f"Generated {i + 1:,} employees..."
            )

    return pd.DataFrame(records)


# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

def save_employees(df):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        OUTPUT_DIR /
        "employees_100k.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print("\n================================")
    print("DATA GENERATION COMPLETE")
    print("================================")

    print(f"Output file: {output_file}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    source_df = load_source_data()

    employees_df = generate_employees(
        source_df,
        NUM_EMPLOYEES
    )

    print("\nFirst 5 generated employees:")
    print(
        employees_df.head().to_string()
    )

    save_employees(employees_df)


if __name__ == "__main__":
    main()
