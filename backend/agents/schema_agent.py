from database.db import (
    get_connection
)


def get_schema_info():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """)

    tables = cursor.fetchall()

    schema = {}

    for table in tables:

        table_name = table[0]

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        schema[table_name] = (
            cursor.fetchall()
        )

    conn.close()

    return schema