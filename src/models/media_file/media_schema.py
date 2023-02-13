from pydantic import BaseModel


class MediaSchema(BaseModel):
    name: str
    link: str
