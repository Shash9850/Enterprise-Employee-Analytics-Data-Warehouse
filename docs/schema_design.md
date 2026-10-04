# Employee Analytics Data Warehouse Schema

## Source Data

The warehouse is generated from the IBM HR Employee Attrition dataset.

Synthetic data generated:

- 100,000 employees
- 3 departments
- 500 projects
- 200,000 employee-project assignments

## Tables

### dim_employee

Stores employee information.

Columns:

- employee_id
- first_name
- last_name
- gender
- age
- marital_status
- education
- education_field
- business_travel
- department_id
- job_role
- job_level
- hire_date

### dim_department

Stores department information.

Columns:

- department_id
- department_name

### dim_project

Stores project information.

Columns:

- project_id
- project_name
- department_id
- start_date
- end_date
- budget
- status

### fact_employee_project

Stores employee project assignments.

Columns:

- assignment_id
- employee_id
- project_id
- allocation_percent
- start_date
- end_date

## Relationships

dim_department
    |
    +---- dim_employee
    |
    +---- dim_project

dim_employee
    |
    +---- fact_employee_project
                |
                +---- dim_project

## Grain

The grain of fact_employee_project is:

One row represents one employee assigned to one project.

## Primary Keys

dim_employee:
employee_id

dim_department:
department_id

dim_project:
project_id

fact_employee_project:
assignment_id

## Foreign Keys

dim_employee.department_id
    -> dim_department.department_id

dim_project.department_id
    -> dim_department.department_id

fact_employee_project.employee_id
    -> dim_employee.employee_id

fact_employee_project.project_id
    -> dim_project.project_id
