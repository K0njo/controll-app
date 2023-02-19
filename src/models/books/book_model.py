from src.database_connection import Base
from sqlalchemy import Integer, Column, String


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(100))
    author = Column(String(100))
    release_year = Column(Integer)
    book_description = Column(String(500))
    linker = Column(String(100), unique=True)
