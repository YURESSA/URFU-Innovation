from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app import Base


class UserTestResult(Base):
    __tablename__ = "user_test_results"

    id = Column(Integer, primary_key=True)
    user_test_id = Column(
        Integer,
        ForeignKey("user_tests.user_test_id", ondelete="CASCADE"),
        nullable=False
    )

    scale = Column(String(10), nullable=False)  # D / I / S / C / или другие
    value = Column(Integer, nullable=False)

    user_test = relationship("UserTest", back_populates="results")
