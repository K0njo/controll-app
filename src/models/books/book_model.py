from src.database_connection import Base
from sqlalchemy import Integer, Column, String


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)

    book_name = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    release_year = Column(Integer, nullable=False)
    book_description = Column(String(500), nullable=False)
    linker = Column(String(100), unique=False)

