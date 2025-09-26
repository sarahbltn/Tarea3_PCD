from sqlalchemy import Column, Integer, String
from sqlalchemy.types import JSON
from database import Base

class Users(Base):
    __tablename__ = "Users"
    
    user_name = Column(String)
    user_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    age = Column(Integer)
    recommendations = Column(JSON)
    ZIP = Column(String)
    
