

import mysql.connector

from config.config import DW_DATABASE_CONFIG

from managers.db_manager import DatabaseConnection



class AnalyticsManager:
    """Handle analytics queries for the application."""

    def __init__(self):
        pass

    def get_connection(self):
        """Return a connection to the data warehouse."""
        return mysql.connector.connect(**DW_DATABASE_CONFIG)




    def get_performance_summary(self):
        """Return overall performance metrics from the data warehouse."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                COUNT(*) AS total_reviews,
                ROUND(AVG(performance_rating), 2) AS average_rating,
                COUNT(DISTINCT employee_key) AS employees_reviewed,
                COUNT(DISTINCT project_key) AS projects_reviewed
            FROM fact_performance_reviews
        """

        try:
            cursor.execute(query)
            row = cursor.fetchone()

            return {
                "total_reviews": row[0],
                "average_rating": row[1],
                "employees_reviewed": row[2],
                "projects_reviewed": row[3]
            }

        finally:
            cursor.close()








    def get_department_performance(self):
        """Return performance metrics grouped by department."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                d.department_name,
                COUNT(*) AS total_reviews,
                ROUND(AVG(f.performance_rating), 2) AS average_rating
            FROM fact_performance_reviews f
            JOIN dim_department d
                ON f.department_key = d.department_key
            GROUP BY
                d.department_name
            ORDER BY
                average_rating DESC
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "department_name": row[0],
                    "total_reviews": row[1],
                    "average_rating": row[2]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()


















    def get_yearly_performance(self):
        """Return yearly performance metrics from the data warehouse."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                d.year,
                COUNT(*) AS total_reviews,
                ROUND(AVG(f.performance_rating), 2) AS average_rating
            FROM fact_performance_reviews f
            JOIN dim_date d
                ON f.date_key = d.date_key
            GROUP BY
                d.year
            ORDER BY
                d.year
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "year": row[0],
                    "total_reviews": row[1],
                    "average_rating": row[2]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()













    def get_top_employees_by_department(self):
        """Return employee performance rankings within each department."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            WITH employee_performance AS (
                SELECT
                    d.department_name,
                    e.employee_key,
                    CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
                    COUNT(*) AS review_count,
                    AVG(f.performance_rating) AS average_rating
                FROM fact_performance_reviews f
                JOIN dim_employee e
                    ON f.employee_key = e.employee_key
                JOIN dim_department d
                    ON f.department_key = d.department_key
                GROUP BY
                    d.department_name,
                    e.employee_key,
                    e.first_name,
                    e.last_name
                HAVING COUNT(*) >= 3
            ),
            ranked_employees AS (
                SELECT
                    department_name,
                    employee_key,
                    employee_name,
                    review_count,
                    ROUND(average_rating, 2) AS average_rating,
                    DENSE_RANK() OVER (
                        PARTITION BY department_name
                        ORDER BY average_rating DESC
                    ) AS department_rank
                FROM employee_performance
            )
            SELECT
                department_name,
                employee_key,
                employee_name,
                review_count,
                average_rating,
                department_rank
            FROM ranked_employees
            WHERE department_rank <= 3
            ORDER BY
                department_name,
                department_rank,
                average_rating DESC,
                review_count DESC
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "department_name": row[0],
                    "employee_key": row[1],
                    "employee_name": row[2],
                    "review_count": row[3],
                    "average_rating": row[4],
                    "department_rank": row[5]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()
















    def get_attrition_summary(self):
        """Return overall employee attrition metrics."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                COUNT(*) AS total_employees,
                SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)
                    AS employees_left,
                SUM(CASE WHEN attrition = 'No' THEN 1 ELSE 0 END)
                    AS active_employees,
                ROUND(
                    100.0 * SUM(
                        CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END
                    ) / COUNT(*),
                    2
                ) AS attrition_rate
            FROM dim_employee
            WHERE is_current = 1
        """

        try:
            cursor.execute(query)
            row = cursor.fetchone()

            return {
                "total_employees": row[0],
                "employees_left": row[1],
                "active_employees": row[2],
                "attrition_rate": row[3]
            }

        finally:
            cursor.close()
            connection.close()






    def get_attrition_by_department(self):
        """Return employee attrition metrics grouped by department."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                d.department_name,
                COUNT(*) AS total_employees,
                SUM(
                    CASE
                        WHEN e.attrition = 'Yes' THEN 1
                        ELSE 0
                    END
                ) AS employees_left,
                SUM(
                    CASE
                        WHEN e.attrition = 'No' THEN 1
                        ELSE 0
                    END
                ) AS active_employees,
                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN e.attrition = 'Yes' THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS attrition_rate
            FROM dim_employee e
            JOIN dim_department d
                ON e.department_key = d.department_key
            WHERE e.is_current = 1
            GROUP BY
                d.department_name
            ORDER BY
                attrition_rate DESC
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "department_name": row[0],
                    "total_employees": row[1],
                    "employees_left": row[2],
                    "active_employees": row[3],
                    "attrition_rate": row[4]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()


















    def get_attrition_by_job_role(self):
        """Return employee attrition metrics grouped by job role."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                e.job_role,
                COUNT(*) AS total_employees,
                SUM(
                    CASE
                        WHEN e.attrition = 'Yes' THEN 1
                        ELSE 0
                    END
                ) AS employees_left,
                SUM(
                    CASE
                        WHEN e.attrition = 'No' THEN 1
                        ELSE 0
                    END
                ) AS active_employees,
                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN e.attrition = 'Yes' THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS attrition_rate
            FROM dim_employee e
            WHERE e.is_current = 1
            GROUP BY
                e.job_role
            ORDER BY
                attrition_rate DESC
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "job_role": row[0],
                    "total_employees": row[1],
                    "employees_left": row[2],
                    "active_employees": row[3],
                    "attrition_rate": row[4]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()









    def get_attrition_by_overtime(self):
        """Return employee attrition metrics grouped by overtime status."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                e.overtime,
                COUNT(*) AS total_employees,
                SUM(
                    CASE
                        WHEN e.attrition = 'Yes' THEN 1
                        ELSE 0
                    END
                ) AS employees_left,
                SUM(
                    CASE
                        WHEN e.attrition = 'No' THEN 1
                        ELSE 0
                    END
                ) AS active_employees,
                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN e.attrition = 'Yes' THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS attrition_rate
            FROM dim_employee e
            WHERE e.is_current = 1
            GROUP BY
                e.overtime
            ORDER BY
                attrition_rate DESC
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "overtime": row[0],
                    "total_employees": row[1],
                    "employees_left": row[2],
                    "active_employees": row[3],
                    "attrition_rate": row[4]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()













    def get_attrition_by_tenure(self):
        """Return employee attrition metrics grouped by tenure."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                CASE
                    WHEN e.years_at_company BETWEEN 0 AND 2
                        THEN '0-2 years'
                    WHEN e.years_at_company BETWEEN 3 AND 5
                        THEN '3-5 years'
                    WHEN e.years_at_company BETWEEN 6 AND 10
                        THEN '6-10 years'
                    WHEN e.years_at_company BETWEEN 11 AND 15
                        THEN '11-15 years'
                    ELSE '16+ years'
                END AS tenure_group,

                COUNT(*) AS total_employees,

                SUM(
                    CASE
                        WHEN e.attrition = 'Yes' THEN 1
                        ELSE 0
                    END
                ) AS employees_left,

                SUM(
                    CASE
                        WHEN e.attrition = 'No' THEN 1
                        ELSE 0
                    END
                ) AS active_employees,

                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN e.attrition = 'Yes' THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS attrition_rate

            FROM dim_employee e

            WHERE e.is_current = 1

            GROUP BY
                CASE
                    WHEN e.years_at_company BETWEEN 0 AND 2
                        THEN '0-2 years'
                    WHEN e.years_at_company BETWEEN 3 AND 5
                        THEN '3-5 years'
                    WHEN e.years_at_company BETWEEN 6 AND 10
                        THEN '6-10 years'
                    WHEN e.years_at_company BETWEEN 11 AND 15
                        THEN '11-15 years'
                    ELSE '16+ years'
                END

            ORDER BY
                MIN(e.years_at_company)
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "tenure_group": row[0],
                    "total_employees": row[1],
                    "employees_left": row[2],
                    "active_employees": row[3],
                    "attrition_rate": row[4]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()






    def get_attrition_risk_indicators(self):
        """Return employees grouped by a transparent attrition risk indicator."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                CASE
                    WHEN
                        (CASE WHEN overtime = 'Yes' THEN 2 ELSE 0 END) +
                        (CASE WHEN years_at_company <= 2 THEN 2 ELSE 0 END) +
                        (CASE WHEN job_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN environment_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN work_life_balance <= 2 THEN 1 ELSE 0 END)
                        >= 6
                        THEN 'Very High'
                    WHEN
                        (CASE WHEN overtime = 'Yes' THEN 2 ELSE 0 END) +
                        (CASE WHEN years_at_company <= 2 THEN 2 ELSE 0 END) +
                        (CASE WHEN job_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN environment_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN work_life_balance <= 2 THEN 1 ELSE 0 END)
                        >= 4
                        THEN 'High'
                    WHEN
                        (CASE WHEN overtime = 'Yes' THEN 2 ELSE 0 END) +
                        (CASE WHEN years_at_company <= 2 THEN 2 ELSE 0 END) +
                        (CASE WHEN job_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN environment_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN work_life_balance <= 2 THEN 1 ELSE 0 END)
                        >= 2
                        THEN 'Moderate'
                    ELSE 'Low'
                END AS risk_level,

                COUNT(*) AS employee_count,

                SUM(
                    CASE
                        WHEN attrition = 'Yes' THEN 1
                        ELSE 0
                    END
                ) AS employees_left,

                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN attrition = 'Yes' THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS attrition_rate

            FROM dim_employee

            WHERE is_current = 1

            GROUP BY
                CASE
                    WHEN
                        (CASE WHEN overtime = 'Yes' THEN 2 ELSE 0 END) +
                        (CASE WHEN years_at_company <= 2 THEN 2 ELSE 0 END) +
                        (CASE WHEN job_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN environment_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN work_life_balance <= 2 THEN 1 ELSE 0 END)
                        >= 6
                        THEN 'Very High'
                    WHEN
                        (CASE WHEN overtime = 'Yes' THEN 2 ELSE 0 END) +
                        (CASE WHEN years_at_company <= 2 THEN 2 ELSE 0 END) +
                        (CASE WHEN job_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN environment_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN work_life_balance <= 2 THEN 1 ELSE 0 END)
                        >= 4
                        THEN 'High'
                    WHEN
                        (CASE WHEN overtime = 'Yes' THEN 2 ELSE 0 END) +
                        (CASE WHEN years_at_company <= 2 THEN 2 ELSE 0 END) +
                        (CASE WHEN job_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN environment_satisfaction <= 2 THEN 1 ELSE 0 END) +
                        (CASE WHEN work_life_balance <= 2 THEN 1 ELSE 0 END)
                        >= 2
                        THEN 'Moderate'
                    ELSE 'Low'
                END

            ORDER BY
                CASE
                    WHEN risk_level = 'Very High' THEN 1
                    WHEN risk_level = 'High' THEN 2
                    WHEN risk_level = 'Moderate' THEN 3
                    ELSE 4
                END
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "risk_level": row[0],
                    "employee_count": row[1],
                    "employees_left": row[2],
                    "attrition_rate": row[3]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()

















    def get_attrition_risk_indicators(self):
        """Return attrition metrics grouped by a rule-based risk indicator."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            WITH risk_scores AS (
                SELECT
                    employee_id,
                    attrition,

                    (
                        CASE
                            WHEN overtime = 'Yes' THEN 2
                            ELSE 0
                        END
                        +
                        CASE
                            WHEN years_at_company <= 2 THEN 2
                            ELSE 0
                        END
                        +
                        CASE
                            WHEN job_satisfaction <= 2 THEN 1
                            ELSE 0
                        END
                        +
                        CASE
                            WHEN environment_satisfaction <= 2 THEN 1
                            ELSE 0
                        END
                        +
                        CASE
                            WHEN work_life_balance <= 2 THEN 1
                            ELSE 0
                        END
                    ) AS risk_score

                FROM dim_employee

                WHERE is_current = 1
            ),

            risk_levels AS (
                SELECT
                    employee_id,
                    attrition,
                    risk_score,

                    CASE
                        WHEN risk_score >= 6 THEN 'Very High'
                        WHEN risk_score >= 4 THEN 'High'
                        WHEN risk_score >= 2 THEN 'Moderate'
                        ELSE 'Low'
                    END AS risk_level

                FROM risk_scores
            )

            SELECT
                risk_level,
                COUNT(*) AS employee_count,

                SUM(
                    CASE
                        WHEN attrition = 'Yes' THEN 1
                        ELSE 0
                    END
                ) AS employees_left,

                ROUND(
                    100.0 *
                    SUM(
                        CASE
                            WHEN attrition = 'Yes' THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS attrition_rate

            FROM risk_levels

            GROUP BY risk_level

            ORDER BY
                CASE
                    WHEN risk_level = 'Very High' THEN 1
                    WHEN risk_level = 'High' THEN 2
                    WHEN risk_level = 'Moderate' THEN 3
                    ELSE 4
                END
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "risk_level": row[0],
                    "employee_count": row[1],
                    "employees_left": row[2],
                    "attrition_rate": row[3]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()














    def get_project_workload(self):
        """Return employee allocation and review workload for each project."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                p.project_id,
                p.project_name,
                COUNT(DISTINCT a.employee_id) AS assigned_employees,
                COUNT(DISTINCT f.review_id) AS performance_reviews,
                ROUND(AVG(f.performance_rating), 2) AS average_rating

            FROM dim_project p

            LEFT JOIN fact_performance_reviews f
                ON p.project_key = f.project_key

            LEFT JOIN greenfield_oltp.assignments a
                ON p.project_id = a.project_id

            GROUP BY
                p.project_id,
                p.project_name

            ORDER BY
                assigned_employees DESC
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "project_id": row[0],
                    "project_name": row[1],
                    "assigned_employees": row[2],
                    "performance_reviews": row[3],
                    "average_rating": row[4]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()












    def get_employee_allocation(self):
        """Return current project allocation metrics for each employee."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                a.employee_id,
                CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
                COUNT(DISTINCT a.project_id) AS active_project_count,
                SUM(a.allocation_percent) AS current_allocation_percent,
                MAX(a.allocation_percent) AS highest_single_allocation

            FROM greenfield_oltp.assignments a

            JOIN greenfield_oltp.employees e
                ON a.employee_id = e.employee_id

            WHERE
                a.start_date <= CURDATE()
                AND a.end_date >= CURDATE()

            GROUP BY
                a.employee_id,
                e.first_name,
                e.last_name

            ORDER BY
                current_allocation_percent DESC
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "employee_id": row[0],
                    "employee_name": row[1],
                    "active_project_count": row[2],
                    "current_allocation_percent": row[3],
                    "highest_single_allocation": row[4]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()











    def get_project_attention_indicators(self):
        """Return project-level workload and performance attention indicators."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            WITH project_metrics AS (
                SELECT
                    p.project_id,
                    p.project_name,

                    COALESCE(a.active_employees, 0)
                        AS active_employees,

                    COALESCE(a.total_allocation_percent, 0)
                        AS total_allocation_percent,

                    r.average_rating

                FROM dim_project p

                LEFT JOIN (
                    SELECT
                        project_id,
                        COUNT(DISTINCT employee_id) AS active_employees,
                        SUM(allocation_percent) AS total_allocation_percent

                    FROM greenfield_oltp.assignments

                    WHERE
                        start_date <= CURDATE()
                        AND end_date >= CURDATE()

                    GROUP BY project_id
                ) a
                    ON p.project_id = a.project_id

                LEFT JOIN (
                    SELECT
                        project_key,
                        AVG(performance_rating) AS average_rating

                    FROM fact_performance_reviews

                    GROUP BY project_key
                ) r
                    ON p.project_key = r.project_key
            ),

            portfolio_baseline AS (
                SELECT
                    AVG(active_employees) AS avg_active_employees,
                    AVG(total_allocation_percent) AS avg_total_allocation,
                    AVG(average_rating) AS avg_project_rating

                FROM project_metrics
            ),

            scored_projects AS (
                SELECT
                    pm.*,

                    (
                        CASE
                            WHEN pm.active_employees >
                                pb.avg_active_employees
                            THEN 1
                            ELSE 0
                        END

                        +

                        CASE
                            WHEN pm.total_allocation_percent >
                                pb.avg_total_allocation
                            THEN 1
                            ELSE 0
                        END

                        +

                        CASE
                            WHEN pm.average_rating IS NOT NULL
                                AND pm.average_rating <
                                    pb.avg_project_rating
                            THEN 1
                            ELSE 0
                        END
                    ) AS attention_score

                FROM project_metrics pm
                CROSS JOIN portfolio_baseline pb
            )

            SELECT
                project_id,
                project_name,
                active_employees,
                ROUND(total_allocation_percent, 2)
                    AS total_allocation_percent,
                ROUND(average_rating, 2)
                    AS average_rating,
                attention_score,

                CASE
                    WHEN attention_score = 3
                        THEN 'High Attention'
                    WHEN attention_score = 2
                        THEN 'Attention'
                    WHEN attention_score = 1
                        THEN 'Watch'
                    ELSE 'Normal'
                END AS attention_level

            FROM scored_projects

            ORDER BY
                attention_score DESC,
                active_employees DESC
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            return [
                {
                    "project_id": row[0],
                    "project_name": row[1],
                    "active_employees": row[2],
                    "total_allocation_percent": row[3],
                    "average_rating": row[4],
                    "attention_score": row[5],
                    "attention_level": row[6]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()











    def get_employee_history(self, employee_id):
        """Return the SCD2 history of an employee in chronological order."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                de.employee_id,
                CONCAT(de.first_name, ' ', de.last_name) AS employee_name,
                de.job_role,
                de.job_level,
                de.monthly_income,
                de.department_key,
                de.start_date,
                de.end_date,
                de.is_current

            FROM dim_employee de

            WHERE de.employee_id = %s

            ORDER BY
                de.start_date;
        """

        try:
            cursor.execute(query, (employee_id,))
            rows = cursor.fetchall()

            return [
                {
                    "employee_id": row[0],
                    "employee_name": row[1],
                    "job_role": row[2],
                    "job_level": row[3],
                    "monthly_income": row[4],
                    "department_key": row[5],
                    "start_date": row[6],
                    "end_date": row[7],
                    "is_current": row[8]
                }
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()















    def get_employee_career_summary(self, employee_id):
        """Return a summary of an employee's career changes from SCD2 history."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            WITH employee_history AS (
                SELECT
                    employee_id,
                    monthly_income,
                    job_level,
                    start_date,
                    ROW_NUMBER() OVER (
                        ORDER BY start_date
                    ) AS version_number
                FROM dim_employee
                WHERE employee_id = %s
            )

            SELECT
                employee_id,
                COUNT(*) AS historical_versions,
                COUNT(*) - 1 AS career_changes,

                MAX(
                    CASE
                        WHEN version_number = 1
                        THEN monthly_income
                    END
                ) AS initial_salary,

                MAX(
                    CASE
                        WHEN version_number = (
                            SELECT MAX(version_number)
                            FROM employee_history
                        )
                        THEN monthly_income
                    END
                ) AS current_salary,

                MAX(
                    CASE
                        WHEN version_number = 1
                        THEN job_level
                    END
                ) AS initial_job_level,

                MAX(
                    CASE
                        WHEN version_number = (
                            SELECT MAX(version_number)
                            FROM employee_history
                        )
                        THEN job_level
                    END
                ) AS current_job_level

            FROM employee_history

            GROUP BY employee_id
        """

        try:
            cursor.execute(query, (employee_id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "employee_id": row[0],
                "historical_versions": row[1],
                "career_changes": row[2],
                "initial_salary": row[3],
                "current_salary": row[4],
                "initial_job_level": row[5],
                "current_job_level": row[6]
            }

        finally:
            cursor.close()
            connection.close()












    def get_scd2_change_summary(self):
        """Return organization-wide employee changes detected from SCD2 history."""
        connection = self.get_connection()
        cursor = connection.cursor()

        query = """
            WITH employee_versions AS (
                SELECT
                    employee_id,
                    department_key,
                    monthly_income,
                    job_level,
                    start_date,

                    LAG(department_key) OVER (
                        PARTITION BY employee_id
                        ORDER BY start_date
                    ) AS previous_department,

                    LAG(monthly_income) OVER (
                        PARTITION BY employee_id
                        ORDER BY start_date
                    ) AS previous_salary,

                    LAG(job_level) OVER (
                        PARTITION BY employee_id
                        ORDER BY start_date
                    ) AS previous_job_level

                FROM dim_employee
            ),

            changes AS (
                SELECT
                    employee_id,

                    CASE
                        WHEN previous_department IS NOT NULL
                            AND department_key <> previous_department
                        THEN 1
                        ELSE 0
                    END AS department_change,

                    CASE
                        WHEN previous_salary IS NOT NULL
                            AND monthly_income > previous_salary
                        THEN 1
                        ELSE 0
                    END AS salary_increase,

                    CASE
                        WHEN previous_job_level IS NOT NULL
                            AND job_level > previous_job_level
                        THEN 1
                        ELSE 0
                    END AS promotion

                FROM employee_versions
            )

            SELECT
                COUNT(DISTINCT CASE
                    WHEN department_change = 1 THEN employee_id
                END) AS employees_with_department_change,

                COUNT(DISTINCT CASE
                    WHEN salary_increase = 1 THEN employee_id
                END) AS employees_with_salary_increase,

                COUNT(DISTINCT CASE
                    WHEN promotion = 1 THEN employee_id
                END) AS employees_with_promotion

            FROM changes
        """

        try:
            cursor.execute(query)
            row = cursor.fetchone()

            return {
                "employees_with_department_change": row[0],
                "employees_with_salary_increase": row[1],
                "employees_with_promotion": row[2]
            }

        finally:
            cursor.close()
            connection.close()