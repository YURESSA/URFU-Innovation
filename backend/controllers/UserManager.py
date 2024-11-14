import sqlite3
from datetime import datetime
from models.UserModel import User


class UserManager:
    def __init__(self, db_name='data/innovate.db3'):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            self._create_users_table(cursor)
            self._create_user_tests_table(cursor)
            self._create_user_answers_table(cursor)
            connection.commit()

    @staticmethod
    def _create_users_table(cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                telegram_id TEXT NOT NULL UNIQUE
            )
        ''')

    @staticmethod
    def _create_user_tests_table(cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_tests (
                user_test_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                test_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (test_id) REFERENCES tests (test_id)
            )
        ''')

    @staticmethod
    def _create_user_answers_table(cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_answers (
                user_answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_test_id INTEGER NOT NULL,
                section1 INTEGER,
                section2 INTEGER,
                section3 INTEGER,
                section4 INTEGER,
                section5 INTEGER,
                section6 INTEGER,
                section7 INTEGER,
                section8 INTEGER,
                FOREIGN KEY (user_test_id) REFERENCES user_tests(user_test_id)
            )
        ''')

    def get_user_id(self, telegram_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT user_id FROM users WHERE telegram_id = ?''', (telegram_id,))
            user = cursor.fetchone()
        return user

    def add_test_to_user(self, user_id, test_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            user_test_id = self._get_existing_user_test(cursor, user_id, test_id)

            if user_test_id:
                self._update_user_test_timestamp(cursor, user_test_id)
            else:
                user_test_id = self._insert_new_user_test(cursor, user_id, test_id)

            connection.commit()
            return user_test_id

    @staticmethod
    def _get_existing_user_test(cursor, user_id, test_id):
        cursor.execute('''SELECT user_test_id FROM user_tests WHERE user_id = ? AND test_id = ?''',
                       (user_id, test_id))
        result = cursor.fetchone()
        return result[0] if result else None

    @staticmethod
    def _update_user_test_timestamp(cursor, user_test_id):
        cursor.execute('''
            UPDATE user_tests
            SET timestamp = ?
            WHERE user_test_id = ?
        ''', (datetime.now(), user_test_id))

    @staticmethod
    def _insert_new_user_test(cursor, user_id, test_id):
        cursor.execute('''
            INSERT INTO user_tests (user_id, test_id)
            VALUES (?, ?)
        ''', (user_id, test_id))
        return cursor.lastrowid

    @staticmethod
    def is_user_exist(telegram_id, cursor):
        cursor.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
        return cursor.fetchone() is not None

    def register_user(self, full_name, phone_number, telegram_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            if self.is_user_exist(telegram_id, cursor):
                return True, "Пользователь с таким Telegram ID уже существует."

            cursor.execute('''
            INSERT
            INTO
            users(full_name, phone_number, telegram_id)
            VALUES(?, ?, ?)
            ''', (full_name, phone_number, telegram_id))
            connection.commit()
            return True, "Пользователь успешно зарегистрирован."
