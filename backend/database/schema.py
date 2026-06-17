from .db import get_connection


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments(
        dept_id INTEGER PRIMARY KEY,
        department_name TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dept_id INTEGER,
        salary INTEGER,

        FOREIGN KEY(dept_id)
        REFERENCES departments(dept_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        project_id INTEGER PRIMARY KEY,
        project_name TEXT,
        budget INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee_projects(
        employee_id INTEGER,
        project_id INTEGER,

        FOREIGN KEY(employee_id)
        REFERENCES employees(id),

        FOREIGN KEY(project_id)
        REFERENCES projects(project_id)
    )
    """)

    conn.commit()
    conn.close()


# ADD THIS BELOW initialize_database()

def seed_data():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT OR IGNORE INTO departments
        VALUES (?,?)
        """,
        [
            (1, "Engineering"),
            (2, "Sales"),
            (3, "HR"),
            (4, "Marketing")
        ]
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO employees
        (id,name,dept_id,salary)
        VALUES (?,?,?,?)
        """,
        [
            (1,"John",1,90000),
            (2,"Sarah",1,85000),
            (3,"Mike",2,60000),
            (4,"Emma",3,55000),
            (5,"David",2,65000)
        ]
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO projects
        VALUES (?,?,?)
        """,
        [
            (1,"AI Platform",500000),
            (2,"CRM Upgrade",200000),
            (3,"HR Portal",100000)
        ]
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO employee_projects
        VALUES (?,?)
        """,
        [
            (1,1),
            (2,1),
            (3,2),
            (4,3)
        ]
    )

    conn.commit()
    conn.close()