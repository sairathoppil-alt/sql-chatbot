from groq import Groq
import os

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)

def ask_assistant(
    question,
    sql="",
    summary="",
    results=None
):

    prompt = f"""
You are Database Copilot Assistant.

You help users with:

- SQL
- DBMS
- Programming
- Data Analysis
- Database Design
- Career Questions
- Project Questions

Current SQL:
{sql}

Current Summary:
{summary}

Current Results:
{results}

User:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (
        response
        .choices[0]
        .message
        .content
    )