from langchain_core.prompts import ChatPromptTemplate

intent_prompt = ChatPromptTemplate.from_template("""
Classify the user request.

Return ONLY one of:

SELECT
INSERT
UPDATE
DELETE

CREATE_TABLE
ALTER_TABLE
DROP_TABLE

SCHEMA_INFO

Question:
{question}
""")