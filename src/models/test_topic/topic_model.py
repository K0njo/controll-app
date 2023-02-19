from src.database_connection import Base
from sqlalchemy import Integer, Column, String, Boolean, JSON


class Topic(Base):
    __tablename__ = 'test_topic'

    id = Column(Integer, primary_key=True)
    question = Column(String(100))
    answer = Column(JSON)


