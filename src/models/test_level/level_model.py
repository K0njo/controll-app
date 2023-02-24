from src.database_connection import Base
from sqlalchemy import Integer, Column, String, JSON


class Level(Base):
    __tablename__ = 'test_level'

    id = Column(Integer, primary_key=True)
    section_name = Column(String(255), nullable=False)
    question = Column(String(255), nullable=False)
    answer = Column(JSON, nullable=False)
    media_file_id = Column(Integer)
