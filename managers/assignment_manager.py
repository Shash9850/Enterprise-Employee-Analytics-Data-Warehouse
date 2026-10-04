from managers.db_manager import DatabaseConnection
from models.assignment import Assignment
import mysql.connector


class AssignmentManager:
    """Manage employee-project assignments in the OLTP database."""

    def __init__(self):
        self.db = DatabaseConnection()

    def get_connection(self):
        return self.db.connect()

    def create_assignment(self, assignment):
        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT COALESCE(MAX(assignment_id), 0) + 1 FROM assignments"
            )
            assignment_id = cursor.fetchone()[0]

            query = """
                INSERT INTO assignments (
                    assignment_id,
                    employee_id,
                    project_id,
                    allocation_percent,
                    start_date,
                    end_date
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                assignment_id,
                assignment.employee_id,
                assignment.project_id,
                assignment.allocation_percent,
                assignment.start_date,
                assignment.end_date,
            )

            cursor.execute(query, values)
            connection.commit()

            assignment.assignment_id = assignment_id
            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Assignment could not be created: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()





    def get_assignment(self, assignment_id):
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT assignment_id, employee_id, project_id,
                   allocation_percent, start_date, end_date
            FROM assignments
            WHERE assignment_id = %s
        """

        try:
            cursor.execute(query, (assignment_id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return Assignment(
                assignment_id=row[0],
                employee_id=row[1],
                project_id=row[2],
                allocation_percent=row[3],
                start_date=row[4],
                end_date=row[5],
            )

        finally:
            cursor.close()

    def get_all_assignments(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT assignment_id, employee_id, project_id,
                   allocation_percent, start_date, end_date
            FROM assignments
            ORDER BY assignment_id DESC
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                Assignment(
                    assignment_id=row[0],
                    employee_id=row[1],
                    project_id=row[2],
                    allocation_percent=row[3],
                    start_date=row[4],
                    end_date=row[5],
                )
                for row in rows
            ]

        finally:
            cursor.close()

    def get_assignment_details(self, active_only=False):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                a.assignment_id,
                a.employee_id,
                CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
                a.project_id,
                p.project_name,
                a.allocation_percent,
                a.start_date,
                a.end_date
            FROM assignments a
            JOIN employees e
                ON a.employee_id = e.employee_id
            JOIN projects p
                ON a.project_id = p.project_id
        """

        if active_only:
            query += """
                WHERE a.start_date <= CURDATE()
                  AND a.end_date >= CURDATE()
            """

        query += " ORDER BY a.assignment_id DESC"

        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def update_assignment(self, assignment):
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE assignments
            SET employee_id = %s,
                project_id = %s,
                allocation_percent = %s,
                start_date = %s,
                end_date = %s
            WHERE assignment_id = %s
        """

        values = (
            assignment.employee_id,
            assignment.project_id,
            assignment.allocation_percent,
            assignment.start_date,
            assignment.end_date,
            assignment.assignment_id,
        )

        try:
            cursor.execute(query, values)

            if cursor.rowcount == 0:
                return False

            connection.commit()
            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Assignment could not be updated: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()

    def delete_assignment(self, assignment_id):
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM assignments
            WHERE assignment_id = %s
        """

        try:
            cursor.execute(query, (assignment_id,))

            if cursor.rowcount == 0:
                return False

            connection.commit()
            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Assignment could not be deleted: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()
