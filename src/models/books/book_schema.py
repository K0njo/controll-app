from pydantic import BaseModel
from typing import Optional


class CreateBook(BaseModel):
    book_name: str
    link: Optional[str]
