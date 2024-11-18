import json
import sqlite3


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
        roles = {}
        with open(self.belbin_test, 'r', encoding='utf-8') as file:
            data = json.load(file)

        roles = {}
        for role in data.get("roles", []):
            section_name = role.get("section_name")
            roles[section_name] = {
                "role_in_team": role.get("role_in_team"),
                "description": role.get("description")
            }

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
