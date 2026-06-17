from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from prompts.summary_prompt import (
    summary_prompt
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def summarize(state):
    if state.get("dangerous"):

        return {

            "summary":
            f"""
    Confirmation required.

    Operation:
    {state['danger_reason']}

    SQL:

    {state['sql_query']}
    """
        }

    sql = state["sql_query"]

    result = state["query_result"]

    # ------------------------
    # Dangerous Operations
    # ------------------------

    if state.get("dangerous"):

        return {
            "summary":
            f"""
⚠️ Warning: Destructive operation executed.

Operation:
{state['danger_reason']}

SQL:
{state['sql_query']}
"""
        }

    # ------------------------
    # INSERT
    # ------------------------

    if sql.lower().startswith("insert"):

        return {
            "summary":
            "Record inserted successfully."
        }

    # ------------------------
    # UPDATE
    # ------------------------

    if sql.lower().startswith("update"):

        return {
            "summary":
            f"{result.get('affected_rows',0)} row(s) updated."
        }

    # ------------------------
    # DELETE
    # ------------------------

    if sql.lower().startswith("delete"):

        return {
            "summary":
            f"{result.get('affected_rows',0)} row(s) deleted."
        }

    # ------------------------
    # CREATE
    # ------------------------

    if sql.lower().startswith("create"):

        return {
            "summary":
            "Table created successfully."
        }

    # ------------------------
    # ALTER
    # ------------------------

    if sql.lower().startswith("alter"):

        return {
            "summary":
            "Table modified successfully."
        }

    # ------------------------
    # DROP
    # ------------------------

    if sql.lower().startswith("drop"):

        return {
            "summary":
            "Table removed successfully."
        }

    # ------------------------
    # SELECT
    # ------------------------

    chain = summary_prompt | llm

    response = chain.invoke({

        "question":
        state["question"],

        "sql":
        state["sql_query"],

        "result":
        result.get(
            "rows",
            []
        )
    })

    return {

        "summary":
        response.content
    }