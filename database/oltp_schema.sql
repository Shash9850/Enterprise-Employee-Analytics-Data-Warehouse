-- ============================================================
-- GREENFIELD MINI PROJECT
-- OLTP DATABASE SCHEMA
-- Employee Performance & Project Management
-- ============================================================

CREATE DATABASE IF NOT EXISTS greenfield_oltp;

USE greenfield_oltp;


-- ============================================================
-- 1. DEPARTMENTS
-- ============================================================

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);


-- ============================================================
-- 2. EMPLOYEES
-- ============================================================

CREATE TABLE employees (
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

    CONSTRAINT fk_employee_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);


-- ============================================================
-- 3. PROJECTS
-- ============================================================

CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    department_id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15, 2),
    status VARCHAR(30),

    CONSTRAINT fk_project_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);


-- ============================================================
-- 4. ASSIGNMENTS
-- ============================================================

CREATE TABLE assignments (
    assignment_id BIGINT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    project_id INT NOT NULL,
    allocation_percent INT NOT NULL,
    start_date DATE,
    end_date DATE,

    CONSTRAINT fk_assignment_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),

    CONSTRAINT fk_assignment_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id),

    CONSTRAINT chk_allocation_percent
        CHECK (allocation_percent BETWEEN 1 AND 100)
);


-- ============================================================
-- 5. REVIEWS
-- ============================================================

CREATE TABLE reviews (
    review_id BIGINT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    project_id INT,
    review_date DATE NOT NULL,
    performance_rating INT,
    reviewer_name VARCHAR(150),
    comments TEXT,

    CONSTRAINT fk_review_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),

    CONSTRAINT fk_review_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id),

    CONSTRAINT chk_performance_rating
        CHECK (performance_rating BETWEEN 1 AND 5)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_employee_department
    ON employees(department_id);

CREATE INDEX idx_project_department
    ON projects(department_id);

CREATE INDEX idx_assignment_employee
    ON assignments(employee_id);

CREATE INDEX idx_assignment_project
    ON assignments(project_id);

CREATE INDEX idx_review_employee
    ON reviews(employee_id);

CREATE INDEX idx_review_project
    ON reviews(project_id);

CREATE INDEX idx_review_date
    ON reviews(review_date);