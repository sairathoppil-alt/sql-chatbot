# setup_db.py

import sqlite3

conn = sqlite3.connect("company.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

employees = [
    (1, "John", "Sales", 50000),
    (2, "Emma", "HR", 60000),
    (3, "David", "Sales", 55000),
    (4, "Sarah", "Engineering", 80000),
    (5, "Mike", "Engineering", 90000)
]

cursor.execute("DELETE FROM employees")

cursor.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?)",
    employees
)

conn.commit()
conn.close()

print("Database created successfully!")