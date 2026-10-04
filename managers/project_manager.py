from managers.db_manager import DatabaseConnection
from models.project import Project
import mysql.connector


class ProjectManager:
    """Handle project-related database operations."""

    def __init__(self):
        """Initialize the project manager."""
        self.db = DatabaseConnection()

    def get_connection(self):
        """Return an active database connection."""
        return self.db.connect()






    def create_project(self, project):
        """Insert a new project into the OLTP database."""

        connection = self.get_connection()
        cursor = connection.cursor()

        try:
            # Generate the next project ID because project_id
            # is not configured as AUTO_INCREMENT.
            cursor.execute(
                """
                SELECT COALESCE(MAX(project_id), 0) + 1
                FROM projects
                """
            )

            next_project_id = cursor.fetchone()[0]

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

            values = (
                next_project_id,
                project.project_name,
                project.department_id,
                project.start_date,
                project.end_date,
                project.budget,
                project.status
            )

            cursor.execute(query, values)
            connection.commit()

            # Keep the generated ID in the Project object.
            project.project_id = next_project_id

            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Project could not be created: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()














    def get_project(self, project_id):
        """Retrieve a project by project ID."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                project_id,
                project_name,
                department_id,
                start_date,
                end_date,
                budget,
                status
            FROM projects
            WHERE project_id = %s
        """

        try:
            cursor.execute(query, (project_id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return Project(
                project_id=row[0],
                project_name=row[1],
                department_id=row[2],
                start_date=row[3],
                end_date=row[4],
                budget=row[5],
                status=row[6]
            )

        finally:
            cursor.close()











    def get_all_projects(self):
        """Retrieve all projects from the OLTP database."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                project_id,
                project_name,
                department_id,
                start_date,
                end_date,
                budget,
                status
            FROM projects
            ORDER BY project_id
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            projects = []

            for row in rows:
                project = Project(
                    project_id=row[0],
                    project_name=row[1],
                    department_id=row[2],
                    start_date=row[3],
                    end_date=row[4],
                    budget=row[5],
                    status=row[6]
                )

                projects.append(project)

            return projects

        finally:
            cursor.close()













    def update_project(self, project):
        """Update an existing project."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE projects
            SET
                project_name = %s,
                department_id = %s,
                start_date = %s,
                end_date = %s,
                budget = %s,
                status = %s
            WHERE project_id = %s
        """

        values = (
            project.project_name,
            project.department_id,
            project.start_date,
            project.end_date,
            project.budget,
            project.status,
            project.project_id
        )

        try:
            cursor.execute(query, values)

            if cursor.rowcount == 0:
                return False

            connection.commit()
            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Project could not be updated: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()














    def delete_project(self, project_id):
        """Delete a project by project ID."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM projects
            WHERE project_id = %s
        """

        try:
            cursor.execute(query, (project_id,))

            if cursor.rowcount == 0:
                return False

            connection.commit()
            return True

        except mysql.connector.IntegrityError as error:
            connection.rollback()
            print(f"Project could not be deleted: {error}")
            return False

        except mysql.connector.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()