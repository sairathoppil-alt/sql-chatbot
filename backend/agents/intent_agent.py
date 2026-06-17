from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from prompts.intent_prompt import (
    intent_prompt
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def detect_intent(state):

    chain = intent_prompt | llm

    response = chain.invoke({
        "question": state["question"]
    })

    intent = (
        response.content
        .strip()
        .upper()
    )

    print("\nIntent:")
    print(intent)

    return {
        "intent": intent
    }