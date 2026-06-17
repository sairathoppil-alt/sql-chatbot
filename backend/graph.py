from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

from agents.intent_agent import (
    detect_intent
)

from agents.sql_agent import (
    generate_sql
)

from agents.validator_agent import (
    validate_sql
)

from agents.summary_agent import (
    summarize
)

from agents.danger_agent import (
    danger_check
)

from database.executor import (
    execute_sql
)


class GraphState(TypedDict):

    question: str

    intent: str

    sql_query: str

    query_result: dict

    summary: str

    dangerous: bool

    danger_reason: str


# -------------------------
# Execute Node
# -------------------------

def execute_query(state):

    if state.get("dangerous"):

        return {

            "query_result": {

                "type":
                "confirmation_required",

                "columns":
                [],

                "rows":
                []
            }
        }

    result = execute_sql(
        state["sql_query"]
    )

    return {

        "query_result":
        result
    }


# -------------------------
# Build Graph
# -------------------------

builder = StateGraph(
    GraphState
)

# Nodes

builder.add_node(
    "detect_intent",
    detect_intent
)

builder.add_node(
    "generate_sql",
    generate_sql
)

builder.add_node(
    "validate_sql",
    validate_sql
)

builder.add_node(
    "danger_check",
    danger_check
)

builder.add_node(
    "execute_query",
    execute_query
)

builder.add_node(
    "summarize",
    summarize
)

# Entry Point

builder.set_entry_point(
    "detect_intent"
)

# Flow

builder.add_edge(
    "detect_intent",
    "generate_sql"
)

builder.add_edge(
    "generate_sql",
    "validate_sql"
)

builder.add_edge(
    "validate_sql",
    "danger_check"
)

builder.add_edge(
    "danger_check",
    "execute_query"
)

builder.add_edge(
    "execute_query",
    "summarize"
)

builder.add_edge(
    "summarize",
    END
)

graph = builder.compile()