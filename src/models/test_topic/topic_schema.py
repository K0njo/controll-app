from pydantic import BaseModel


class TopiSchema(BaseModel):
    question: str
    answer: str