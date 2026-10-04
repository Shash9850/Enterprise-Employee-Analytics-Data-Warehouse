import pandas as pd


EMPLOYEE_FILE = "data/generated/employees_100k.csv"
REVIEW_FILE = "data/generated/reviews.csv"


def main():
    """Validate generated reviews against employee employment dates."""

    print("Loading employees...")
    employees = pd.read_csv(EMPLOYEE_FILE)

    print("Loading reviews...")
    reviews = pd.read_csv(REVIEW_FILE)

    employees["hire_date"] = pd.to_datetime(employees["hire_date"])
    reviews["review_date"] = pd.to_datetime(reviews["review_date"])

    validation = reviews.merge(
        employees[["employee_id", "hire_date"]],
        on="employee_id",
        how="left"
    )

    missing_employees = validation["hire_date"].isna().sum()

    reviews_before_hire = (
        validation["review_date"] < validation["hire_date"]
    ).sum()

    reviews_on_or_after_hire = (
        validation["review_date"] >= validation["hire_date"]
    ).sum()

    print("\n================================")
    print("REVIEW DATA VALIDATION")
    print("================================")

    print(f"Total reviews: {len(reviews):,}")
    print(f"Reviews with missing employee: {missing_employees:,}")
    print(f"Reviews before employee hire date: {reviews_before_hire:,}")
    print(
        f"Reviews on/after employee hire date: "
        f"{reviews_on_or_after_hire:,}"
    )

    if reviews_before_hire > 0:
        print("\nInvalid examples:")

        invalid = validation[
            validation["review_date"] < validation["hire_date"]
        ]

        print(
            invalid[
                [
                    "review_id",
                    "employee_id",
                    "hire_date",
                    "review_date"
                ]
            ].head(10).to_string(index=False)
        )

    if (
        missing_employees == 0
        and reviews_before_hire == 0
        and reviews_on_or_after_hire == len(reviews)
    ):
        print("\n✅ REVIEW DATA IS VALID")
    else:
        print("\n❌ REVIEW DATA NEEDS ATTENTION")


if __name__ == "__main__":
    main()