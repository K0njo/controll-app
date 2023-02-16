from pydantic import BaseModel
from typing import Dict

class TopicSchema(BaseModel):
    question: str
    answer: Dict[str, str]