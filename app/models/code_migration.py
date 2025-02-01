from sqlalchemy import Column, Integer, String
from app.models import Base

class CodeMigration(Base):
    __tablename__ = "code_migrations"
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), unique=True, nullable=False)
