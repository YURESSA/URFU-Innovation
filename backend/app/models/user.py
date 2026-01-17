from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    telegram_id = Column(String, unique=True, nullable=False)

    tests = relationship("UserTest", back_populates="user")
