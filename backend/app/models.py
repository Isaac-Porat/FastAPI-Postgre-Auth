from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
