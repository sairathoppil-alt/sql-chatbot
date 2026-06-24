from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import (
    ChatRequest,
    ConfirmRequest,
    AskRequest
)

from graph import graph

from database.schema import (
    initialize_database,
    seed_data
)

from database.db import (
    get_connection
)

from database.executor import (
    execute_sql
)

from agents.assistant_agent import (
    ask_assistant
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


# -----------------------------
# Root
# -----------------------------

@app.get("/")
def root():

    return {
        "message":
        "Database Copilot Running"
    }


# -----------------------------
# Schema Viewer
# -----------------------------

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

        schema[table] = (
            cursor.fetchall()
        )

    conn.close()

    return schema


# -----------------------------
# Main SQL Copilot
# -----------------------------

@app.post("/chat")
def chat(
    request: ChatRequest
):

    try:

        result = graph.invoke({
            "question":
            request.question
        })

        return {

            "intent":
            result.get(
                "intent"
            ),

            "sql":
            result.get(
                "sql_query"
            ),

            "columns":
            result.get(
                "query_result",
                {}
            ).get(
                "columns",
                []
            ),

            "rows":
            result.get(
                "query_result",
                {}
            ).get(
                "rows",
                []
            ),

            "summary":
            result.get(
                "summary"
            )
        }

    except Exception as e:

        return {
            "error":
            str(e)
        }


# -----------------------------
# Confirm Dangerous SQL
# -----------------------------

@app.post("/confirm")
def confirm_sql(
    request: ConfirmRequest
):

    try:

        result = execute_sql(
            request.sql
        )

        return {

            "success":
            True,

            "result":
            result
        }

    except Exception as e:

        return {

            "success":
            False,

            "error":
            str(e)
        }


# -----------------------------
# AI Assistant
# -----------------------------

@app.post("/ask")
def ask_ai(
    request: AskRequest
):

    try:

        answer = ask_assistant(

            request.question,

            request.sql,

            request.summary,

            request.results
        )

        return {
            "answer":
            answer
        }

    except Exception as e:

        return {
            "answer":
            f"Error: {str(e)}"
        }