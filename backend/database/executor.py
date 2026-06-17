from .db import get_connection


def execute_sql(
    query,
    dangerous=False
):

    conn = get_connection()

    cursor = conn.cursor()

    print("\nExecuting SQL:")
    print(query)

    cursor.execute(query)

    if query.lower().startswith("select"):

        columns = []

        if cursor.description:

            columns = [
                c[0]
                for c in cursor.description
            ]

        rows = cursor.fetchall()

        conn.close()

        return {

            "type":
            "select",

            "columns":
            columns,

            "rows":
            rows
        }

    conn.commit()

    affected = cursor.rowcount

    conn.close()

    return {

        "type":
        "write",

        "affected_rows":
        affected,

        "columns":
        [],

        "rows":
        []
    }