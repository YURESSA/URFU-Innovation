import json
from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from app.database import SessionLocal
from app.models.test import TestEnum
from app.models.user import User
from app.models.user_answer import UserAnswer
from app.models.user_test import UserTest


class TestManager:
    def __init__(self, session_factory=None, belbin_test='data/belbin/belbin.json'):
        self.session_factory = session_factory or SessionLocal
        self.belbin_test = belbin_test

    def get_all_questions(self):
        with open(self.belbin_test, 'r', encoding='utf-8') as file:
            data = json.load(file)

        questions = [
            {"block_name": block.get("block_name"), "questions": block.get("questions", [])}
            for block in data.get("questions", [])
        ]
        return questions

    def get_roles_and_descriptions(self):
        with open(self.belbin_test, 'r', encoding='utf-8') as file:
            data = json.load(file)

        roles = {}
        for role in data.get("roles", []):
            section_name = role.get("section_name")
            roles[section_name] = {
                "role_in_team": role.get("role_in_team"),
                "description": role.get("description"),
                "file_name": role.get("file_name"),
                "strong-side": role.get("strong-side"),
                "weak-side": role.get("weak-side"),
                "goal": role.get("goal"),
                "term": role.get("term"),
                "recommendations": role.get("recommendations"),
            }
        return roles

    def get_tests(self):
        return [(t.display_name, t.url) for t in TestEnum]

    def save_user_answers(self, user_test_id, data_percentages):
        section_values = {f"section{i}": data_percentages.get(f"section{i}", 0) for i in range(1, 9)}

        with self.session_factory() as session:
            user_answer = session.scalars(
                select(UserAnswer).where(UserAnswer.user_test_id == user_test_id)
            ).first()

            if user_answer:
                for key, value in section_values.items():
                    setattr(user_answer, key, value)
            else:
                user_answer = UserAnswer(user_test_id=user_test_id, **section_values)
                session.add(user_answer)

            session.commit()

    def get_filtered_results(self, telegram_id=None, test_name=None, start_date=None, end_date=None):
        roles_dict = self.get_roles_and_descriptions()
        roles = [v["role_in_team"] for v in roles_dict.values()]

        with self.session_factory() as session:
            query = select(UserTest).options(
                joinedload(UserTest.user),
                joinedload(UserTest.answers)
            )

            filters = []

            if telegram_id:
                filters.append(User.telegram_id == telegram_id)

            if test_name:
                try:
                    enum_value = TestEnum[test_name]
                    filters.append(UserTest.test_id == enum_value)
                except KeyError:
                    return []

            if start_date:
                start_dt = self._parse_date(start_date)
                if start_dt:
                    filters.append(UserTest.timestamp >= start_dt)

            if end_date:
                end_dt = self._parse_date(end_date)
                if end_dt:
                    filters.append(UserTest.timestamp <= end_dt)

            if filters:
                query = query.join(User).where(and_(*filters))
            else:
                query = query.join(User)

            query = query.order_by(UserTest.timestamp.desc())
            results = session.scalars(query).all()

            return self._format_results(results, roles)

    @staticmethod
    def _parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None

    @staticmethod
    def _format_results(results, roles):
        formatted = []
        for ut in results:
            sections = {role: getattr(ut.answers, f"section{i + 1}") for i, role in enumerate(roles)}
            formatted.append({
                "full_name": ut.user.full_name,
                "phone_number": ut.user.phone_number,
                "telegram_id": ut.user.telegram_id,
                "test_name": ut.test_id.display_name,
                "timestamp": ut.timestamp,
                "sections": sections
            })
        return formatted

