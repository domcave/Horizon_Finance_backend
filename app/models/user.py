from sqlalchemy import Column, Integer, String
from app.models import Base
from app import bcrypt

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    access_token = Column(String(255))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)