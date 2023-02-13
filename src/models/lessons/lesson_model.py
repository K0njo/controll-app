from src.database_connection import Base
from sqlalchemy import Integer, Column, String, Boolean


class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True)
    level = Column(String)
    topic_name = Column(String)
    topic_description = Column(String)
    media_file_id = Column(Integer)
    test_topic_id = Column(Integer)
