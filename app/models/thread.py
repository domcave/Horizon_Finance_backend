from sqlalchemy import Column, Integer, String
from app.models import Base

class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    thread = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)