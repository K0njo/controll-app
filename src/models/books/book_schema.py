from pydantic import BaseModel, validator
from typing import Optional


class CreateBook(BaseModel):
    book_name: str
    author: str
    release_year: int
    book_description: Optional[str]
    linker: Optional[str]

    @validator('release_year')
    def validator_year(cls, val):
        if len(str(val)) != 4:
            raise ValueError('Year must be a 4-digit integer')
            return val


