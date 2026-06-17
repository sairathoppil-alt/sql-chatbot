from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from prompts.sql_prompt import (
    sql_prompt
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def generate_sql(state):

    chain = sql_prompt | llm

    response = chain.invoke({
        "question": state["question"]
    })

    sql = response.content.strip()

    sql = sql.replace(
        "```sql",
        ""
    )

    sql = sql.replace(
        "```",
        ""
    )

    sql = sql.strip()

    print("\nGenerated SQL:")
    print(sql)

    return {
        "sql_query": sql
    }