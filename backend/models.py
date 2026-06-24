from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ConfirmRequest(BaseModel):
    sql: str


class AskRequest(BaseModel):
    question: str
    sql: str = ""
    summary: str = ""
    results: dict = {}