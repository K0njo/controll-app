from pydantic import BaseModel

class LessonSchema(BaseModel):
    level: str
    topic_name: str
    topic_description: str
