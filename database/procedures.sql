/*
    Enterprise Employee Analytics & Data Warehouse System
    Stored Procedure: Incremental OLTP -> OLAP Load

    Purpose:
    - Move newly added data from OLTP into the existing DWH.
    - Preserve existing SCD Type 2 employee history.
    - Avoid duplicate departments, employees, projects, dates, and reviews.
    - Load fact reviews using the employee dimension version
      that was valid on the review date.

    IMPORTANT:
    This procedure does NOT:
    - DROP tables
    - TRUNCATE tables
    - DELETE existing DWH data
    - Overwrite existing SCD2 employee history
*/

USE greenfield_dw;

DELIMITER $$

CREATE PROCEDURE sp_load_olap_incremental()
BEGIN

    /*
        If anything fails during the load, roll back all
        changes made by this procedure execution.
    */
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;


    /* =========================================================
       1. LOAD NEW DEPARTMENTS
       ========================================================= */

    INSERT INTO greenfield_dw.dim_department
        (department_id, department_name)
    SELECT
        d.department_id,
        d.department_name
    FROM greenfield_oltp.departments d
    LEFT JOIN greenfield_dw.dim_department dd
        ON dd.department_id = d.department_id
    WHERE dd.department_id IS NULL;


    /* =========================================================
       2. LOAD NEW EMPLOYEES
       
       Only employees that do not already exist in the DWH
       are inserted.

       Existing SCD2 records are NOT updated here.
       ========================================================= */

    INSERT INTO greenfield_dw.dim_employee
    (
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
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        e.gender,
        e.job_role,
        e.job_level,
        e.monthly_income,
        dd.department_key,
        e.hire_date,
        NULL,
        1,
        e.attrition,
        e.overtime,
        e.years_at_company,
        e.job_satisfaction,
        e.environment_satisfaction,
        e.work_life_balance,
        e.job_involvement,
        e.relationship_satisfaction
    FROM greenfield_oltp.employees e
    INNER JOIN greenfield_dw.dim_department dd
        ON dd.department_id = e.department_id
    LEFT JOIN greenfield_dw.dim_employee de
        ON de.employee_id = e.employee_id
    WHERE de.employee_id IS NULL
      AND e.hire_date IS NOT NULL;


    /* =========================================================
       3. LOAD NEW PROJECTS
       ========================================================= */

    INSERT INTO greenfield_dw.dim_project
    (
        project_id,
        project_name,
        department_key,
        start_date,
        end_date,
        budget,
        status
    )
    SELECT
        p.project_id,
        p.project_name,
        dd.department_key,
        p.start_date,
        p.end_date,
        p.budget,
        p.status
    FROM greenfield_oltp.projects p
    INNER JOIN greenfield_dw.dim_department dd
        ON dd.department_id = p.department_id
    LEFT JOIN greenfield_dw.dim_project dp
        ON dp.project_id = p.project_id
    WHERE dp.project_id IS NULL;


    /* =========================================================
       4. LOAD NEW REVIEW DATES
       
       date_key format:
       YYYYMMDD
       
       Example:
       2026-10-04 -> 20261004
       ========================================================= */

    INSERT INTO greenfield_dw.dim_date
    (
        date_key,
        full_date,
        day,
        month,
        month_name,
        quarter,
        year
    )
    SELECT DISTINCT
        YEAR(r.review_date) * 10000
            + MONTH(r.review_date) * 100
            + DAY(r.review_date) AS date_key,

        r.review_date AS full_date,

        DAY(r.review_date) AS day,

        MONTH(r.review_date) AS month,

        MONTHNAME(r.review_date) AS month_name,

        QUARTER(r.review_date) AS quarter,

        YEAR(r.review_date) AS year

    FROM greenfield_oltp.reviews r

    LEFT JOIN greenfield_dw.dim_date d
        ON d.full_date = r.review_date

    WHERE d.full_date IS NULL;


    /* =========================================================
       5. LOAD NEW PERFORMANCE REVIEWS INTO FACT TABLE
       
       IMPORTANT:
       The employee dimension row is selected according
       to the REVIEW DATE.

       This preserves SCD Type 2 historical accuracy.
       ========================================================= */

    INSERT INTO greenfield_dw.fact_performance_reviews
    (
        review_id,
        employee_key,
        project_key,
        date_key,
        department_key,
        performance_rating,
        review_count
    )
    SELECT
        r.review_id,

        de.employee_key,

        dp.project_key,

        dd_date.date_key,

        de.department_key,

        r.performance_rating,

        1 AS review_count

    FROM greenfield_oltp.reviews r

    INNER JOIN greenfield_dw.dim_employee de
        ON de.employee_id = r.employee_id

        /*
            Select the SCD2 employee version that was
            valid when the review occurred.
        */
        AND de.start_date <= r.review_date
        AND (
            de.end_date IS NULL
            OR r.review_date <= de.end_date
        )

    LEFT JOIN greenfield_dw.dim_project dp
        ON dp.project_id = r.project_id

    INNER JOIN greenfield_dw.dim_date dd_date
        ON dd_date.full_date = r.review_date

    LEFT JOIN greenfield_dw.fact_performance_reviews f
        ON f.review_id = r.review_id

    WHERE f.review_id IS NULL;


    /* =========================================================
       6. COMMIT ONLY AFTER ALL LOADS SUCCEED
       ========================================================= */

    COMMIT;

END$$

DELIMITER ;