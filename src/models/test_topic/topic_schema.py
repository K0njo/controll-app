from pydantic import BaseModel, validator
from typing import Dict

class TopicSchema(BaseModel):
    question: str
    answer: Dict[str, str]

    @validator('answer')
    def validator_answer(cls, value):
        if len(value) != 4:
            raise ValueError('Answer field must contain 4 answers ')
        return value