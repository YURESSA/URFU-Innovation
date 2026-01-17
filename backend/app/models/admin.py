import bcrypt
from sqlalchemy import Column, String

from app.database import Base


class Admin(Base):
    __tablename__ = "admins"

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    role = Column(String, default="admin")

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def check_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
