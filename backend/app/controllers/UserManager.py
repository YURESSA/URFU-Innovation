from datetime import datetime

from sqlalchemy import select

from app.database import SessionLocal
from app.models.test import TestEnum
from app.models.user import User
from app.models.user_test import UserTest


class UserManager:
    def __init__(self, session_factory=None):
        self.session_factory = session_factory or SessionLocal

    def get_user_by_telegram(self, telegram_id: str):
        with self.session_factory() as session:
            return session.scalars(select(User).where(User.telegram_id == telegram_id)).first()

    def get_user_id(self, telegram_id: str):
        with self.session_factory() as session:
            user = session.scalars(select(User).where(User.telegram_id == telegram_id)).first()
            return user.user_id if user else None

    def is_user_exist(self, telegram_id: str):
        with self.session_factory() as session:
            return session.scalars(select(User).where(User.telegram_id == telegram_id)).first() is not None

    def register_user(self, full_name, phone_number, telegram_id, password):
        with self.session_factory() as session:
            existing_user = session.scalars(select(User).where(User.telegram_id == telegram_id)).first()
            if existing_user:
                return False, "Пользователь с таким Telegram ID уже существует."

            user = User(full_name=full_name, phone_number=phone_number, telegram_id=telegram_id)
            user.set_password(password)
            session.add(user)
            session.commit()
            return True, "Пользователь успешно зарегистрирован."

    def add_test_to_user(self, user_id: int, test_id: int):
        id_to_enum = {
            1: TestEnum.BELBIN
        }

        try:
            test_enum = id_to_enum[test_id]
        except KeyError:
            raise ValueError(f"Нет теста с id={test_id}")

        with self.session_factory() as session:
            user_test = session.scalars(
                select(UserTest).where(
                    UserTest.user_id == user_id,
                    UserTest.test_id == test_enum
                )
            ).first()

            if user_test:
                user_test.timestamp = datetime.now()
            else:
                user_test = UserTest(user_id=user_id, test_id=test_enum)
                session.add(user_test)

            session.commit()
            return user_test.user_test_id
