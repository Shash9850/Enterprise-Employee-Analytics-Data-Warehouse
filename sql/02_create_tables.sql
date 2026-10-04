-- ============================================================
-- Employee Performance & Workforce Intelligence
-- Table Creation
-- ============================================================


-- ============================================================
-- OLTP DATABASE
-- ============================================================

USE greenfield_oltp;


-- ------------------------------------------------------------
-- Departments
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);


-- ------------------------------------------------------------
-- Employees
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS employees (
    employee_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    gender VARCHAR(20),
    age INT,
    department_id INT NOT NULL,
    job_role VARCHAR(100),
    job_level INT,
    monthly_income DECIMAL(12, 2),
    hire_date DATE,
    attrition VARCHAR(10),
    overtime VARCHAR(10),
    years_at_company INT,
    job_satisfaction INT,
    environment_satisfaction INT,
    work_life_balance INT,
    job_involvement INT,
    relationship_satisfaction INT,
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);


-- ------------------------------------------------------------
-- Projects
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    department_id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15, 2),
    status VARCHAR(30),
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);


-- ------------------------------------------------------------
-- Assignments
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS assignments (
    assignment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    project_id INT NOT NULL,
    allocation_percent INT NOT NULL,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),
    FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
);


-- ------------------------------------------------------------
-- Reviews
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS reviews (
    review_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    project_id INT,
    review_date DATE NOT NULL,
    performance_rating INT,
    reviewer_name VARCHAR(150),
    comments TEXT,
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),
    FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
);


-- ============================================================
-- DATA WAREHOUSE DATABASE
-- ============================================================

USE greenfield_dw;


-- ------------------------------------------------------------
-- Department Dimension
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_department (
    department_key INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT NOT NULL UNIQUE,
    department_name VARCHAR(100) NOT NULL
);


-- ------------------------------------------------------------
-- Employee Dimension - SCD Type 2
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_employee (
    employee_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    job_role VARCHAR(100),
    job_level INT,
    monthly_income DECIMAL(12, 2),
    department_key INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    is_current TINYINT(1) DEFAULT 1,
    attrition VARCHAR(10),
    overtime VARCHAR(10),
    years_at_company INT,
    job_satisfaction INT,
    environment_satisfaction INT,
    work_life_balance INT,
    job_involvement INT,
    relationship_satisfaction INT,
    FOREIGN KEY (department_key)
        REFERENCES dim_department(department_key)
);


-- ------------------------------------------------------------
-- Project Dimension
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_project (
    project_key INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL UNIQUE,
    project_name VARCHAR(255) NOT NULL,
    department_key INT NOT NULL,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15, 2),
    status VARCHAR(30),
    FOREIGN KEY (department_key)
        REFERENCES dim_department(department_key)
);


-- ------------------------------------------------------------
-- Date Dimension
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL
);


-- ------------------------------------------------------------
-- Performance Review Fact
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS fact_performance_reviews (
    performance_review_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    review_id BIGINT NOT NULL UNIQUE,
    employee_key BIGINT NOT NULL,
    project_key INT,
    date_key INT NOT NULL,
    department_key INT NOT NULL,
    performance_rating INT,
    review_count INT NOT NULL DEFAULT 1,
    FOREIGN KEY (employee_key)
        REFERENCES dim_employee(employee_key),
    FOREIGN KEY (project_key)
        REFERENCES dim_project(project_key),
    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),
    FOREIGN KEY (department_key)
        REFERENCES dim_department(department_key)
);