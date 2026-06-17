from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ConfirmRequest(BaseModel):
    sql: str