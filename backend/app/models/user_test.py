from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.test import TestEnum


class UserTest(Base):
    __tablename__ = "user_tests"

    user_test_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    test_id = Column(SQLEnum(TestEnum), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="tests")
    answers = relationship("UserAnswer", back_populates="user_test", uselist=False)
    results = relationship(
        "UserTestResult",
        back_populates="user_test",
        cascade="all, delete-orphan"
    )
