from langchain_core.prompts import ChatPromptTemplate

sql_prompt = ChatPromptTemplate.from_template("""
You are an expert SQLite database engineer.

Database Schema:

departments(
    dept_id INTEGER PRIMARY KEY,
    department_name TEXT
)

employees(
    id INTEGER PRIMARY KEY,
    name TEXT,
    dept_id INTEGER,
    salary INTEGER
)

projects(
    project_id INTEGER PRIMARY KEY,
    project_name TEXT,
    budget INTEGER
)

employee_projects(
    employee_id INTEGER,
    project_id INTEGER
)

Relationships:

employees.dept_id -> departments.dept_id

employee_projects.employee_id -> employees.id

employee_projects.project_id -> projects.project_id

Rules:

- Return ONLY SQL
- No markdown
- No explanations
- SQLite syntax only

Question:
{question}
""")