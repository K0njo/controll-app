from pydantic import BaseModel


class LevelSchema(BaseModel):
    question: str
    section_name: str
    answer: str