FORBIDDEN = [

    "ATTACH",

    "DETACH",

    "VACUUM",

    "PRAGMA"
]


def validate_sql(state):

    sql = state["sql_query"]

    sql_upper = sql.upper()

    for keyword in FORBIDDEN:

        if keyword in sql_upper:

            raise Exception(
                f"Forbidden SQL operation: {keyword}"
            )

    return {}