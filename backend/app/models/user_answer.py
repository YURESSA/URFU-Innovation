from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class UserAnswer(Base):
    __tablename__ = "user_answers"

    user_answer_id = Column(Integer, primary_key=True, autoincrement=True)
    user_test_id = Column(Integer, ForeignKey("user_tests.user_test_id"))

    section1 = Column(Integer)
    section2 = Column(Integer)
    section3 = Column(Integer)
    section4 = Column(Integer)
    section5 = Column(Integer)
    section6 = Column(Integer)
    section7 = Column(Integer)
    section8 = Column(Integer)

    user_test = relationship("UserTest", back_populates="answers")
