from sqlalchemy import Integer, Column, String, Boolean
from src.database_connection import Base

class User(Base):
    __tablename__ = 'sys_users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True, index=True)
    username = Column(String(30), unique=True, index=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    hash_password = Column(String(100))
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f'Name %s. Email %s. username %s. first_name %s. last_name %s. hash_password %s. is_active %s.' \
            % (
                self.email, self.email, self.username, self.first_name, self.last_name, self.hash_password,
                self.is_active)
