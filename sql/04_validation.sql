-- ============================================================
-- Employee Performance & Workforce Intelligence
-- Data Validation
-- ============================================================


-- ============================================================
-- 1. OLTP ROW COUNTS
-- ============================================================

USE greenfield_oltp;

SELECT
    'departments' AS table_name,
    COUNT(*) AS row_count
FROM departments

UNION ALL

SELECT
    'employees',
    COUNT(*)
FROM employees

UNION ALL

SELECT
    'projects',
    COUNT(*)
FROM projects

UNION ALL

SELECT
    'assignments',
    COUNT(*)
FROM assignments

UNION ALL

SELECT
    'reviews',
    COUNT(*)
FROM reviews;


-- ============================================================
-- 2. EMPLOYEE ID DUPLICATES
-- ============================================================

SELECT
    employee_id,
    COUNT(*) AS employee_count
FROM employees
GROUP BY employee_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 3. EMPLOYEE EMAIL DUPLICATES
-- ============================================================

SELECT
    email,
    COUNT(*) AS email_count
FROM employees
GROUP BY email
HAVING COUNT(*) > 1;


-- ============================================================
-- 4. ORPHAN EMPLOYEE DEPARTMENT RECORDS
-- ============================================================

SELECT
    e.employee_id,
    e.department_id
FROM employees e
LEFT JOIN departments d
    ON e.department_id = d.department_id
WHERE d.department_id IS NULL;


-- ============================================================
-- 5. ORPHAN ASSIGNMENTS
-- ============================================================

SELECT
    a.assignment_id
FROM assignments a
LEFT JOIN employees e
    ON a.employee_id = e.employee_id
LEFT JOIN projects p
    ON a.project_id = p.project_id
WHERE e.employee_id IS NULL
   OR p.project_id IS NULL;


-- ============================================================
-- 6. ORPHAN REVIEWS
-- ============================================================

SELECT
    r.review_id
FROM reviews r
LEFT JOIN employees e
    ON r.employee_id = e.employee_id
LEFT JOIN projects p
    ON r.project_id = p.project_id
WHERE e.employee_id IS NULL
   OR p.project_id IS NULL;


-- ============================================================
-- 7. INVALID REVIEW RATINGS
-- ============================================================

SELECT
    review_id,
    rating
FROM reviews
WHERE rating NOT BETWEEN 1 AND 5
   OR rating IS NULL;


-- ============================================================
-- 8. REVIEW EMPLOYEE HIRE-DATE VALIDATION
-- ============================================================

SELECT
    r.review_id,
    r.employee_id,
    r.review_date,
    e.hire_date
FROM reviews r
JOIN employees e
    ON r.employee_id = e.employee_id
WHERE r.review_date < e.hire_date;


-- ============================================================
-- DATA WAREHOUSE VALIDATION
-- ============================================================

USE greenfield_dw;


-- ============================================================
-- 9. DWH ROW COUNTS
-- ============================================================

SELECT
    'dim_employee' AS table_name,
    COUNT(*) AS row_count
FROM dim_employee

UNION ALL

SELECT
    'dim_department',
    COUNT(*)
FROM dim_department

UNION ALL

SELECT
    'dim_project',
    COUNT(*)
FROM dim_project

UNION ALL

SELECT
    'dim_date',
    COUNT(*)
FROM dim_date

UNION ALL

SELECT
    'fact_performance_reviews',
    COUNT(*)
FROM fact_performance_reviews;


-- ============================================================
-- 10. ONE CURRENT SCD2 VERSION PER EMPLOYEE
-- ============================================================

SELECT
    employee_id,
    COUNT(*) AS current_versions
FROM dim_employee
WHERE is_current = 1
GROUP BY employee_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 11. SCD2 CURRENT VERSION VALIDATION
-- ============================================================

SELECT
    employee_id
FROM dim_employee
GROUP BY employee_id
HAVING SUM(is_current = 1) <> 1;


-- ============================================================
-- 12. SCD2 DATE VALIDATION
-- ============================================================

SELECT
    employee_id,
    employee_key,
    start_date,
    end_date,
    is_current
FROM dim_employee
WHERE end_date IS NOT NULL
  AND end_date < start_date;


-- ============================================================
-- 13. SCD2 CURRENT RECORD DATE VALIDATION
-- ============================================================

SELECT
    employee_id,
    employee_key,
    start_date,
    end_date,
    is_current
FROM dim_employee
WHERE is_current = 1
  AND end_date IS NOT NULL;


-- ============================================================
-- 14. DWH EMPLOYEE DEPARTMENT VALIDATION
-- ============================================================

SELECT
    e.employee_id,
    e.department_key
FROM dim_employee e
LEFT JOIN dim_department d
    ON e.department_key = d.department_key
WHERE d.department_key IS NULL;


-- ============================================================
-- 15. FACT EMPLOYEE KEY VALIDATION
-- ============================================================

SELECT
    f.performance_review_key,
    f.employee_key
FROM fact_performance_reviews f
LEFT JOIN dim_employee e
    ON f.employee_key = e.employee_key
WHERE e.employee_key IS NULL;


-- ============================================================
-- 16. FACT PROJECT KEY VALIDATION
-- ============================================================

SELECT
    f.performance_review_key,
    f.project_key
FROM fact_performance_reviews f
LEFT JOIN dim_project p
    ON f.project_key = p.project_key
WHERE p.project_key IS NULL;


-- ============================================================
-- 17. FACT DATE KEY VALIDATION
-- ============================================================

SELECT
    f.performance_review_key,
    f.date_key
FROM fact_performance_reviews f
LEFT JOIN dim_date d
    ON f.date_key = d.date_key
WHERE d.date_key IS NULL;


-- ============================================================
-- 18. FACT DEPARTMENT KEY VALIDATION
-- ============================================================

SELECT
    f.performance_review_key,
    f.department_key
FROM fact_performance_reviews f
LEFT JOIN dim_department d
    ON f.department_key = d.department_key
WHERE d.department_key IS NULL;


-- ============================================================
-- 19. INVALID FACT RATINGS
-- ============================================================

SELECT
    performance_review_key,
    review_id,
    performance_rating
FROM fact_performance_reviews
WHERE performance_rating NOT BETWEEN 1 AND 5
   OR performance_rating IS NULL;


-- ============================================================
-- 20. DUPLICATE REVIEW IDs IN FACT TABLE
-- ============================================================

SELECT
    review_id,
    COUNT(*) AS review_count
FROM fact_performance_reviews
GROUP BY review_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 21. FACT ROW COUNT
-- ============================================================

SELECT
    COUNT(*) AS total_fact_reviews
FROM fact_performance_reviews;


-- ============================================================
-- 22. SCD2 SUMMARY
-- ============================================================

SELECT
    COUNT(DISTINCT employee_id) AS total_employees,
    COUNT(*) AS total_dimension_rows,
    SUM(is_current = 1) AS current_versions,
    SUM(is_current = 0) AS historical_versions
FROM dim_employee;