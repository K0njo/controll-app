from src.database_connection import Base
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from src.models.media_file.medi_model import Media
from src.models.test_topic.topic_model import Topic

class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(Integer, primary_key=True)
    level = Column(String(30))
    topic_name = Column(String(100))
    topic_description = Column(String(3000))
    media_file_id = Column(Integer, ForeignKey("media.id"))
    test_topic_id = Column(Integer, ForeignKey("test_topic.id"))
