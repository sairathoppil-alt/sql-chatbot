from langchain_core.prompts import ChatPromptTemplate

summary_prompt = ChatPromptTemplate.from_template("""
Question:
{question}

SQL:
{sql}

Result:
{result}

Give a short business-friendly summary.

Maximum 3 sentences.
""")