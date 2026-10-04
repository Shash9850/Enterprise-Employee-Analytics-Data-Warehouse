from datetime import date, timedelta

from managers.db_manager import DatabaseConnection


class SCD2Manager:
    """Handle employee SCD Type 2 changes in the data warehouse."""

    def __init__(self):
        """Initialize the SCD2 manager."""
        self.db = DatabaseConnection()

    def get_connection(self):
        """Return an active database connection."""
        return self.db.connect()

    def update_employee_department(self, employee_id, new_department_id):
        """Create a new Dim_Employee version when the department changes."""

        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Get the employee's latest details from OLTP.
            cursor.execute(
                """
                SELECT
                    employee_id,
                    first_name,
                    last_name,
                    gender,
                    department_id,
                    job_role,
                    job_level,
                    monthly_income,
                    attrition,
                    overtime,
                    years_at_company,
                    job_satisfaction,
                    environment_satisfaction,
                    work_life_balance,
                    job_involvement,
                    relationship_satisfaction
                FROM employees
                WHERE employee_id = %s
                """,
                (employee_id,)
            )

            employee = cursor.fetchone()

            if employee is None:
                return False

            # Get the new department's surrogate key.
            cursor.execute(
                """
                SELECT department_key
                FROM greenfield_dw.dim_department
                WHERE department_id = %s
                """,
                (new_department_id,)
            )

            department = cursor.fetchone()

            if department is None:
                return False

            new_department_key = department["department_key"]

            # Get the current SCD2 version.
            cursor.execute(
                """
                SELECT
                    employee_key,
                    department_key
                FROM greenfield_dw.dim_employee
                WHERE employee_id = %s
                  AND is_current = 1
                """,
                (employee_id,)
            )

            current_version = cursor.fetchone()

            if current_version is None:
                return False

            # If the department has not changed, no new version is needed.
            if current_version["department_key"] == new_department_key:
                return True

            today = date.today()
            previous_day = today - timedelta(days=1)

            # Close the existing SCD2 version.
            cursor.execute(
                """
                UPDATE greenfield_dw.dim_employee
                SET
                    end_date = %s,
                    is_current = 0
                WHERE employee_id = %s
                  AND is_current = 1
                """,
                (previous_day, employee_id)
            )

            # Insert the new SCD2 version.
            cursor.execute(
                """
                INSERT INTO greenfield_dw.dim_employee (
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
                    is_current,
                    attrition,
                    overtime,
                    years_at_company,
                    job_satisfaction,
                    environment_satisfaction,
                    work_life_balance,
                    job_involvement,
                    relationship_satisfaction
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, NULL,
                    1, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                """,
                (
                    employee["employee_id"],
                    employee["first_name"],
                    employee["last_name"],
                    employee["gender"],
                    employee["job_role"],
                    employee["job_level"],
                    employee["monthly_income"],
                    new_department_key,
                    today,
                    employee["attrition"],
                    employee["overtime"],
                    employee["years_at_company"],
                    employee["job_satisfaction"],
                    employee["environment_satisfaction"],
                    employee["work_life_balance"],
                    employee["job_involvement"],
                    employee["relationship_satisfaction"]
                )
            )

            connection.commit()
            return True

        except Exception as error:
            connection.rollback()
            print(f"SCD2 update failed: {error}")
            return False

        finally:
            cursor.close()