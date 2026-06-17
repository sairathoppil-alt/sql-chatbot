from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import sqlite3
import os

# ---------------------
# Load Environment Variables
# ---------------------

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------------
# Create FastAPI App
# ---------------------

app = FastAPI()

# ---------------------
# CORS Configuration
# ---------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# Request Model
# ---------------------

class ChatRequest(BaseModel):
    question: str

# ---------------------
# Database Schema
# ---------------------

SCHEMA = """
Table: employees

Columns:
id INTEGER
name TEXT
department TEXT
salary INTEGER
"""

# ---------------------
# Generate SQL from User Question
# ---------------------

def generate_sql(question):

    prompt = f"""
You are an SQL expert.

Database Schema:

{SCHEMA}

Rules:
- Return ONLY SQL
- Use SQLite syntax
- Only generate SELECT statements
- For text comparisons, use LOWER()
- Make department and name searches case-insensitive

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql = response.choices[0].message.content.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql

# ---------------------
# Execute SQL
# ---------------------

def execute_query(sql):

    blocked_words = [
        "drop",
        "delete",
        "update",
        "alter",
        "truncate",
        "insert"
    ]

    sql_lower = sql.lower()

    for word in blocked_words:
        if word in sql_lower:
            raise Exception(
                f"Blocked SQL command detected: {word}"
            )

    if not sql_lower.startswith("select"):
        raise Exception(
            "Only SELECT statements are allowed"
        )

    conn = sqlite3.connect("company.db")

    cursor = conn.cursor()

    cursor.execute(sql)

    result = cursor.fetchall()

    conn.close()

    return result

# ---------------------
# Convert Result to English
# ---------------------

def summarize_result(question, result):

    prompt = f"""
User Question:
{question}

Database Result:
{result}

Explain the result in simple English.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# ---------------------
# Home Route
# ---------------------

@app.get("/")
def home():
    return {
        "message": "SQL Chatbot Running Successfully"
    }

# ---------------------
# Chat Route
# ---------------------

@app.post("/chat")
def chat(req: ChatRequest):

    sql = generate_sql(req.question)

    print("\nGenerated SQL:")
    print(sql)
    print("-------------------")

    result = execute_query(sql)

    summary = summarize_result(
        req.question,
        result
    )

    return {
        "question": req.question,
        "generated_sql": sql,
        "database_result": result,
        "answer": summary
    }