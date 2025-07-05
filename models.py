# models.py
from sqlalchemy import Column, Integer, String, Text
from database import Base

class Candidate(Base):
    __tablename__ = 'candidates'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Text, index=True)
    skills = Column(Text)
    experience = Column(Text)
    source = Column(Text)
