from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware
)

from models import (
    ChatRequest,
    ConfirmRequest
)

from graph import graph

from database.schema import (
    initialize_database,
    seed_data
)

from database.db import (
    get_connection
)

app = FastAPI()

initialize_database()
seed_data()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():

    return {
        "message":
        "Database Copilot Running"
    }


@app.get("/schema")
def get_schema():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """)

    tables = [
        row[0]
        for row in cursor.fetchall()
    ]

    schema = {}

    for table in tables:

        cursor.execute(
            f"PRAGMA table_info({table})"
        )

        columns = cursor.fetchall()

        schema[table] = columns

    conn.close()

    return schema


@app.post("/chat")
def chat(
    request: ChatRequest
):

    result = graph.invoke({
        "question":
        request.question
    })

    return {

        "intent":
        result["intent"],

        "sql":
        result["sql_query"],

        "columns":
        result["query_result"]["columns"],

        "rows":
        result["query_result"]["rows"],

        "summary":
        result["summary"]
    }
@app.post("/confirm")
def confirm_sql(
    request: ConfirmRequest
):

    from database.executor import (
        execute_sql
    )

    result = execute_sql(
        request.sql
    )

    return {
        "success": True,
        "result": result
    }