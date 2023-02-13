from src.database_connection import Base
from sqlalchemy import Integer, Column, String


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(100), unique=True)
    linker = Column(String(100), unique=False)
