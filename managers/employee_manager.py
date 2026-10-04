from managers.db_manager import DatabaseConnection
from models import employee
from models.employee import Employee
import mysql.connector

class EmployeeManager:
    """Handle employee-related database operations."""

    def __init__(self):
        """Initialize the employee manager."""
        self.db = DatabaseConnection()

    def get_connection(self):
        """Return an active database connection."""
        return self.db.connect()

    def create_employee(self, employee):
        """Insert a new employee into the OLTP database."""
        connection = self.get_connection()
        cursor = connection.cursor()

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
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """

        values = (
            employee.employee_id,
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.gender,
            employee.age,
            employee.department_id,
            employee.job_role,
            employee.job_level,
            employee.monthly_income,
            employee.hire_date,
            employee.attrition
        )

        try:
            cursor.execute(query, values)
            connection.commit()
            return True
        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Employee could not be created: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()




    def get_employee(self, employee_id):
        """Retrieve an employee by employee ID."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
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
            FROM employees
            WHERE employee_id = %s
        """

        try:
            cursor.execute(query, (employee_id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return Employee(
                employee_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                gender=row[4],
                age=row[5],
                department_id=row[6],
                job_role=row[7],
                job_level=row[8],
                monthly_income=row[9],
                hire_date=row[10],
                attrition=row[11]
            )

        finally:
            cursor.close()









    def get_all_employees(self):
        """Retrieve all employees from the OLTP database."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
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
            FROM employees
            ORDER BY employee_id
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            employees = []

            for row in rows:
                employee = Employee(
                    employee_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    gender=row[4],
                    age=row[5],
                    department_id=row[6],
                    job_role=row[7],
                    job_level=row[8],
                    monthly_income=row[9],
                    hire_date=row[10],
                    attrition=row[11]
                )

                employees.append(employee)

            return employees

        finally:
            cursor.close()











    def update_employee(self, employee):
        """Update an existing employee's non-historical details."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE employees
            SET
                first_name = %s,
                last_name = %s,
                email = %s,
                gender = %s,
                age = %s,
                department_id = %s,
                job_role = %s,
                job_level = %s,
                monthly_income = %s,
                hire_date = %s,
                attrition = %s
            WHERE employee_id = %s
                """

        values = (
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.gender,
            employee.age,
            employee.department_id,
            employee.job_role,
            employee.job_level,
            employee.monthly_income,
            employee.hire_date,
            employee.attrition,
            employee.employee_id
        )

        try:
            cursor.execute(query, values)

            if cursor.rowcount == 0:
                connection.rollback()
                return False

            connection.commit()
            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Employee could not be updated: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()












    def delete_employee(self, employee_id):
        """Delete an employee from the OLTP database."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM employees
            WHERE employee_id = %s
        """

        try:
            cursor.execute(query, (employee_id,))

            if cursor.rowcount == 0:
                return False

            connection.commit()
            return True

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Employee could not be deleted: {error}")
            return False

        finally:
            cursor.close()