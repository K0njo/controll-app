from pydantic import BaseModel
from typing import Optional


class CreateBook(BaseModel):
    book_name: str
    author: str
    release_year: int
    book_description: Optional[str]
    linker: Optional[str]




