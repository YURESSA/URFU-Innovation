import sqlite3


class DatabaseController:
    def __init__(self, db_name='data/innovate.db3'):
        self.db_name = db_name

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_all_questions(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
            SELECT b.block_name, q.question_text
            FROM belbin_question_blocks b
            JOIN belbin_question q ON q.block_id = b.block_id
            ''')
            results = cursor.fetchall()

        questions = []
        for block_name, question_text in results:
            block = next((item for item in questions if item['block_name'] == block_name), None)
            if block is None:
                block = {'block_name': block_name, 'questions': []}
                questions.append(block)
            block['questions'].append(question_text)

        return questions

    def get_tests(self):
        query = 'SELECT test_name, test_url FROM tests'
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def get_roles_and_descriptions(self):
        roles = {}
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT section_name, role_in_team, description FROM roles_table''')
            rows = cursor.fetchall()
            for row in rows:
                section_name, role_in_team, description = row
                roles[section_name] = {'role_in_team': role_in_team, 'description': description}
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
