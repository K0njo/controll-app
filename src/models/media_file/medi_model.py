from src.database_connection import Base
from sqlalchemy import Integer, Column, String, Boolean
class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    link = Column(String(255))
