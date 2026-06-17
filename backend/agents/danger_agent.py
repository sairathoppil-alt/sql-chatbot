DANGEROUS_KEYWORDS = [

    "DELETE",

    "DROP TABLE",

    "DROP COLUMN",

    "TRUNCATE"
]


def danger_check(state):

    sql = state["sql_query"].upper()

    dangerous = False

    reason = None

    for keyword in DANGEROUS_KEYWORDS:

        if keyword in sql:

            dangerous = True

            reason = keyword

            break

    return {

        "dangerous":
        dangerous,

        "danger_reason":
        reason
    }