# Enterprise Employee Analytics & Data Warehouse System

## Project Overview

The Enterprise Employee Analytics & Data Warehouse System is an end-to-end data engineering and analytics project developed as part of the Rising Stars Batch 11 Greenfield Mini-Project.

The system demonstrates how enterprise employee data can be generated, stored, transformed, historized, and analyzed using Python, pandas, Faker, MySQL, SQL, Data Warehousing, Object-Oriented Programming, and Streamlit.

The project implements both an OLTP database for operational transactions and an OLAP/Data Warehouse using a star schema for analytical workloads.

## Objectives

- Generate a large-scale employee dataset using Python, pandas, and Faker.
- Scale the IBM HR Employee Attrition dataset to 100,000+ employees.
- Generate related departments, projects, assignments, and performance reviews.
- Store operational data in a normalized MySQL OLTP database.
- Build a dimensional Data Warehouse for analytics.
- Implement Slowly Changing Dimension Type 2 (SCD Type 2) for employee history.
- Implement SQL stored procedures for incremental Data Warehouse loading.
- Develop a Python OOP-based application layer.
- Build an interactive Streamlit application.
- Provide analytical dashboards for employee performance, attrition, workload, and project insights.
- Validate data integrity across the OLTP and Data Warehouse systems.

## Technology Stack

- Python 3
- pandas
- Faker
- MySQL
- SQL
- Streamlit
- Plotly
- Altair
- Git
- GitHub
- Draw.io

## System Architecture

The system follows an end-to-end data pipeline:

IBM HR Dataset
        |
        v
Python + pandas + Faker
        |
        v
Synthetic Data Generation
        |
        +----------------+
        |                |
        v                v
Employees          Related Data
                   - Departments
                   - Projects
                   - Assignments
                   - Reviews
        |                |
        +-------+--------+
                |
                v
        MySQL OLTP Database
                |
                v
        ETL / Incremental Loading
                |
                v
        MySQL Data Warehouse
                |
                +-------------------+
                |                   |
                v                   v
        Dimension Tables       Fact Table
                |
                v
        Analytics Manager
                |
                v
        Streamlit Dashboard

## Dataset Generation

The project uses the IBM HR Employee Attrition dataset as the base dataset.

Python was used to generate a larger enterprise-scale dataset using pandas and Faker.

The generated dataset contains:

- 100,000 employees
- 3 departments
- 500 projects
- 200,003 performance reviews

The generated employee dataset contains 100,000 unique employee records.

Historical employee events were also generated to support historical analysis and SCD Type 2 implementation.

## OLTP Database

The OLTP database is named:

greenfield_oltp

The database follows a normalized relational design.

### Employees

Stores employee information including:

- Employee ID
- First Name
- Last Name
- Email
- Gender
- Age
- Department
- Job Role
- Job Level
- Monthly Income
- Hire Date
- Attrition
- Overtime
- Years at Company
- Job Satisfaction
- Environment Satisfaction
- Work Life Balance
- Job Involvement
- Relationship Satisfaction

### Departments

Stores department information.

### Projects

Stores project information including:

- Project ID
- Project Name
- Department
- Start Date
- End Date
- Budget
- Status

### Reviews

Stores employee performance review information.

### Assignments

Stores employee-project assignments and allocation percentages.

## Data Warehouse

The Data Warehouse is named:

greenfield_dw

A Star Schema is implemented for analytical workloads.

### Dimension Tables

- Dim_Employee
- Dim_Department
- Dim_Project
- Dim_Date

### Fact Table

- Fact_PerformanceReviews

The fact table stores employee performance review events and connects them to the relevant dimension records.

## Surrogate Keys

Surrogate keys are used in the Data Warehouse dimension tables.

The business employee ID is maintained as the business key, while employee_key is used as the surrogate key.

This allows multiple historical versions of the same employee to exist in Dim_Employee.

## Slowly Changing Dimension Type 2

The project implements Slowly Changing Dimension Type 2 for employee history.

When an employee's department changes, the previous dimension record is not overwritten.

Instead:

1. The existing record is closed.
2. The end_date is populated.
3. is_current is changed to 0.
4. A new employee dimension record is created.
5. The new record receives a new surrogate key.
6. The new record has is_current = 1.

Example:

Employee E000001

Old Version:
Start Date: 2016-06-04
End Date: 2026-10-03
Current: 0

New Version:
Start Date: 2026-10-04
End Date: NULL
Current: 1

This approach preserves historical employee information and allows analytical queries to identify the employee attributes that were valid at a particular point in time.

## Historical Fact Mapping

Performance reviews are mapped to the correct employee dimension version based on the review date.

For example, a review dated 2026-10-03 is mapped to the previous employee dimension version, while a review dated 2026-10-04 is mapped to the new current version.

This demonstrates the practical use of SCD Type 2 in a Data Warehouse environment.

## ETL and Incremental Loading

The project contains an incremental Data Warehouse loading stored procedure:

sp_load_olap_incremental

The procedure loads newly available:

- Departments
- Employees
- Projects
- Dates
- Reviews

into the Data Warehouse without recreating the entire database.

The procedure:

- Prevents duplicate records.
- Preserves SCD Type 2 history.
- Resolves the appropriate employee dimension version.
- Loads fact records.
- Uses transaction handling.
- Rolls back changes when an error occurs.

The procedure was tested successfully.

The final Data Warehouse contains:

- 3 departments
- 108,690 employee dimension records including historical versions
- 500 projects
- 2,182 date records
- 200,003 performance review fact records

All OLTP reviews were successfully represented in the Data Warehouse fact table.

## Python Object-Oriented Design

The application layer follows Python Object-Oriented Programming principles.

### Models

Entity classes represent major business objects:

- Employee
- Project
- Review
- Assignment

### Managers

Dedicated manager classes handle database operations:

- EmployeeManager
- ProjectManager
- ReviewManager
- AssignmentManager
- SCD2Manager
- AnalyticsManager
- DatabaseConnection

This separates application logic from database operations and improves code organization and maintainability.

## Singleton Database Connection

The project implements a Singleton-style database connection through the DatabaseConnection class.

The connection manager provides a reusable database connection and handles connection management.

This avoids creating unnecessary database connection objects throughout the application.

## CRUD Operations

The application supports CRUD operations for the major business entities.

### Employee

- Create
- Read
- Update
- Delete

### Project

- Create
- Read
- Update
- Delete

### Review

- Create
- Read
- Update
- Delete

### Assignment

- Create
- Read
- Update
- Delete

Employee department changes are handled separately through the SCD2 manager so that historical information is preserved.

## Streamlit Application

The project provides an interactive Streamlit application.

The application includes:

- Dashboard
- Employee Management
- Employee Onboarding
- Project Management
- Reviews
- Assignments
- Analytics

The application allows users to interact with employee, project, assignment, and review data through a graphical interface.

## Analytics

The analytics layer queries the Data Warehouse for analytical reporting.

The project includes analytical capabilities such as:

### Performance Analysis

- Overall performance summary
- Department performance
- Yearly performance
- Top-performing employees

### Attrition Analysis

- Overall attrition
- Attrition by department
- Attrition by job role
- Attrition by overtime

### Employee and Project Analytics

The analytics layer also provides employee and project-level analytical insights.

Advanced SQL techniques such as Common Table Expressions, window functions, ranking, aggregation, filtering, and joins are used for analytical queries.

## SQL Features

The project demonstrates the following SQL concepts:

- Primary Keys
- Foreign Keys
- Unique Constraints
- Indexes
- Joins
- Aggregations
- Common Table Expressions
- Window Functions
- Stored Procedures
- Transactions
- Conditional Logic
- Incremental Loading
- Dimensional Modelling

Window functions are used for analytical tasks such as ranking employees within departments.

## Data Validation

The project was validated using multiple data integrity checks.

| Validation | Result |
|---|---:|
| Employees | 100,000 |
| Projects | 500 |
| Reviews | 200,003 |
| Departments | 3 |
| Dim Employee Records | 108,690 |
| Dim Date Records | 2,182 |
| Missing Reviews in DWH | 0 |
| Duplicate Review IDs | 0 |
| Employee-before-hire review violations | 0 |
| Orphan Dimension Keys | 0 |

The additional Dim_Employee records represent historical SCD Type 2 versions.

## Project Structure

Mini_Project_DW-main/
|
├── app.py
├── README.md
├── requirements.txt
|
├── config/
│   └── config.py
|
├── data/
│   ├── generated/
│   └── raw/
|
├── database/
│   ├── analytics.sql
│   ├── dw_schema.sql
│   ├── oltp_schema.sql
│   └── procedures.sql
|
├── docs/
│   └── schema_design.md
|
├── etl/
│   ├── etl_pipeline.py
│   ├── generate_related_data.py
│   ├── inspect_data.py
│   └── synthesizer.py
|
├── managers/
│   ├── analytics_manager.py
│   ├── assignment_manager.py
│   ├── db_manager.py
│   ├── employee_manager.py
│   ├── project_manager.py
│   ├── review_manager.py
│   └── scd2_manager.py
|
├── models/
│   ├── employee.py
│   ├── project.py
│   ├── review.py
│   └── assignment.py
|
├── pages/
│   ├── dashboard.py
│   ├── employee_management.py
│   ├── onboarding.py
│   ├── projects.py
│   ├── reviews.py
│   └── assignments.py
|
└── sql/
    ├── 01_create_database.sql
    ├── 02_create_tables.sql
    ├── 03_load_data.sql
    └── 04_validation.sql

## Installation

Clone the repository:

git clone <repository-url>

Navigate to the project directory:

cd Mini_Project_DW-main

Install the required Python packages:

pip install -r requirements.txt

Configure the MySQL database connection using environment variables:

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=<your_username>
MYSQL_PASSWORD=<your_password>
MYSQL_DATABASE=greenfield_oltp
MYSQL_DW_DATABASE=greenfield_dw

Database credentials should not be committed to GitHub.

## Database Setup

Create the required databases and tables using the SQL scripts provided in the project.

The SQL scripts include:

- Database creation
- Table creation
- Data loading
- Data validation

The Data Warehouse schema and stored procedure are available in the database directory.

## Running the Application

Start the Streamlit application using:

streamlit run app.py

The application will open in the browser.

## Testing and Validation

The project was tested at multiple levels.

### Data Generation Testing

- Verified employee count.
- Verified unique employee IDs.
- Verified generated data completeness.

### Database Testing

- Verified OLTP row counts.
- Verified foreign-key relationships.
- Verified Data Warehouse dimensions.
- Verified fact table records.

### SCD Type 2 Testing

- Tested an employee department change.
- Verified historical record closure.
- Verified creation of a new current version.
- Verified that fact records map to the correct historical employee version.

### Incremental Loading Testing

- Executed sp_load_olap_incremental.
- Verified newly available reviews were loaded.
- Verified no duplicate fact records were introduced.
- Verified all OLTP reviews were represented in the fact table.

## Deployment

The application is designed to be deployed using Streamlit Community Cloud.

The Streamlit entry point is:

app.py

For cloud deployment, database credentials should be configured using deployment secrets rather than committing credentials to the GitHub repository.

The deployed application requires a cloud-accessible MySQL database because a Streamlit Cloud application cannot directly connect to a MySQL database running only on a developer's local machine.

## Documentation

Project documentation includes:

- Database schema documentation
- OLTP design
- Data Warehouse design
- SCD Type 2 implementation
- ETL pipeline
- Application architecture
- Setup instructions
- Analytics implementation

Editable architecture and database diagrams can be maintained using Draw.io.

## Conclusion

The Enterprise Employee Analytics & Data Warehouse System demonstrates an end-to-end enterprise data engineering workflow, starting from synthetic data generation and continuing through operational storage, ETL, dimensional modelling, historical data management, analytics, and visualization.

The project combines Python OOP, pandas, Faker, MySQL, SQL, Data Warehousing, SCD Type 2, stored procedures, and Streamlit into a single enterprise-style system.

The system demonstrates how transactional employee data can be transformed into a scalable analytical platform while preserving historical information for accurate reporting and decision-making.