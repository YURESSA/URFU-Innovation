import json
import sqlite3
from datetime import datetime


class TestManager:
    def __init__(self, db_name='data/innovate.db3', belbin_test='data/belbin/belbin.json'):
        self.db_name = db_name
        self.belbin_test = belbin_test

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_all_questions(self):
        with open(self.belbin_test, 'r', encoding='utf-8') as file:
            data = json.load(file)

        questions = []
        for block in data.get("questions", []):
            block_name = block.get("block_name")
            block_questions = block.get("questions", [])
            questions.append({
                "block_name": block_name,
                "questions": block_questions
            })

        return questions

    def get_tests(self):
        query = 'SELECT test_name, test_url FROM tests'
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()

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
                'goal': role.get("goal"),
                'term': role.get("term"),
                "recommendations": role.get("recommendations"),
            }
        print(roles)
        return roles

    def save_user_answers(self, user_test_id, data_percentages):
        section_values = {key: data_percentages.get(key, 0) for key in ['section1', 'section2', 'section3', 'section4',
                                                                        'section5', 'section6', 'section7', 'section8']}

        with self.get_connection() as connection:
            cursor = connection.cursor()
            if self.is_record_exists(cursor, user_test_id):
                self.update_user_answers(cursor, user_test_id, section_values)
            else:
                self.insert_user_answers(cursor, user_test_id, section_values)

            connection.commit()

    @staticmethod
    def is_record_exists(cursor, user_test_id):
        cursor.execute('''
            SELECT COUNT(*) FROM user_answers WHERE user_test_id = ?
        ''', (user_test_id,))
        return cursor.fetchone()[0] > 0

    @staticmethod
    def update_user_answers(cursor, user_test_id, section_values):
        cursor.execute('''
            UPDATE user_answers
            SET section1 = ?, section2 = ?, section3 = ?, section4 = ?, section5 = ?,
                section6 = ?, section7 = ?, section8 = ?
            WHERE user_test_id = ?
        ''', (
            section_values['section1'], section_values['section2'], section_values['section3'],
            section_values['section4'], section_values['section5'], section_values['section6'],
            section_values['section7'], section_values['section8'], user_test_id
        ))

    @staticmethod
    def insert_user_answers(cursor, user_test_id, section_values):
        cursor.execute('''
            INSERT INTO user_answers (user_test_id, section1, section2, section3, section4,
             section5, section6, section7, section8)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_test_id, section_values['section1'], section_values['section2'], section_values['section3'],
              section_values['section4'], section_values['section5'], section_values['section6'],
              section_values['section7'], section_values['section8']
              ))

    def get_filtered_results(self, telegram_id=None, test_name=None, start_date=None, end_date=None):
        query, params = self._build_query(telegram_id, test_name, start_date, end_date)

        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()

        roles = [v.get('role_in_team') for k, v in self.get_roles_and_descriptions().items()]
        return self._format_results(results, roles)

    def _build_query(self, telegram_id, test_name, start_date, end_date):
        query = '''
            SELECT u.full_name, u.phone_number, u.telegram_id, t.test_name, ut.timestamp, 
                   ua.section1, ua.section2, ua.section3, 
                   ua.section4, ua.section5, ua.section6, 
                   ua.section7, ua.section8
            FROM user_tests ut
            JOIN users u ON u.user_id = ut.user_id
            JOIN user_answers ua ON ua.user_test_id = ut.user_test_id
            JOIN tests t ON t.test_id = ut.test_id
            ORDER BY ut.timestamp desc 
        '''
        params = []

        if telegram_id:
            query += " AND u.telegram_id = ?"
            params.append(telegram_id)
        if test_name:
            query += " AND t.test_name = ?"
            params.append(test_name)
        if start_date:
            start_date = self._parse_date(start_date)
            query += " AND ut.timestamp >= ?"
            params.append(start_date)
        if end_date:
            end_date = self._parse_date(end_date)
            query += " AND ut.timestamp <= ?"
            params.append(end_date)

        return query, params

    @staticmethod
    def _parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M')
        except ValueError:
            return None

    @staticmethod
    def _format_results(results, roles):
        return [{
            "full_name": r[0],
            "phone_number": r[1],
            "telegram_id": r[2],
            "test_name": r[3],
            "timestamp": r[4],
            "sections": {role: count for count, role in zip(r[5:], roles)}
        } for r in results]