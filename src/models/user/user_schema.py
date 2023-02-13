from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str