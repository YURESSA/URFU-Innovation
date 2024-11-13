import sqlite3
from datetime import datetime

from models.UserModel import User


class UserManager:
    def __init__(self, db_name='data/innovate.db3'):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        """Подключение к базе данных"""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Создание таблицы пользователей, если она еще не существует"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    telegram_id TEXT NOT NULL UNIQUE
                )
            ''')
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
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS user_answers (
                                user_answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_test_id INTEGER NOT NULL,
                                section1 TEXT,
                                section2 TEXT,
                                section3 TEXT,
                                section4 TEXT,
                                section5 TEXT,
                                section6 TEXT,
                                section7 TEXT,
                                section8 TEXT,
                                FOREIGN KEY (user_test_id) REFERENCES user_tests(user_test_id)
                            )
            ''')
            connection.commit()

    def save_user_answers(self, user_test_id, section_data):
        """
        Сохранение или обновление данных секций в таблице UserAnswers
        :param user_test_id: ID теста, связанного с пользователем
        :param section_data: словарь с результатами по секциям, например:
                             {"1_section": "6", "2_section": "10", ...}
        """
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT user_answer_id FROM user_answers WHERE user_test_id = ?', (user_test_id,))
            existing_answer = cursor.fetchone()

            if existing_answer:
                cursor.execute('''
                    UPDATE user_answers
                    SET section1 = ?, section2 = ?, section3 = ?, section4 = ?, 
                        section5 = ?, section6 = ?, section7 = ?
                    WHERE user_test_id = ?
                ''', (
                    section_data.get("section1"),
                    section_data.get("section2"),
                    section_data.get("section3"),
                    section_data.get("section4"),
                    section_data.get("section5"),
                    section_data.get("section6"),
                    section_data.get("section7"),
                    user_test_id
                ))
            else:
                cursor.execute('''
                    INSERT INTO user_answers (user_test_id, section1, section2, section3,
                                              section4, section5, section6, section7, section8)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_test_id,
                    section_data.get("section1"),
                    section_data.get("section2"),
                    section_data.get("section3"),
                    section_data.get("section4"),
                    section_data.get("section5"),
                    section_data.get("section6"),
                    section_data.get("section7"),
                    section_data.get("section8")
                ))

            connection.commit()

    def get_user_id(self, telegram_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT user_id FROM users WHERE telegram_id = ?', (telegram_id,))
            user = cursor.fetchone()
        return user

    def add_test_to_user(self, user_id, test_id):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT user_test_id FROM user_tests WHERE user_id = ? AND test_id = ?', (user_id, test_id))
            existing_test = cursor.fetchone()

            if existing_test:
                cursor.execute('''
                    UPDATE user_tests
                    SET timestamp = ?
                    WHERE user_test_id = ?
                ''', (datetime.now(), existing_test[0]))
                connection.commit()
                return existing_test[0]
            else:
                cursor.execute('''
                    INSERT INTO user_tests (user_id, test_id)
                    VALUES (?, ?)
                ''', (user_id, test_id))
                connection.commit()
                return cursor.lastrowid

    @staticmethod
    def is_user_exist(telegram_id, cursor):
        """Проверка, существует ли пользователь с таким telegram_id"""
        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        return cursor.fetchone() is not None

    def register_user(self, full_name, phone_number, telegram_id):
        """Регистрация нового пользователя в базе данных"""
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
