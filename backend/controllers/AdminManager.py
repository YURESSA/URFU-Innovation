import sqlite3

from models.AdminModel import Admin


class AdminManager:
    def __init__(self, db_name='data/innovate.db3'):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'admin'
                )
            ''')
            connection.commit()

    @staticmethod
    def is_admin_exist(username, cursor):
        cursor.execute('SELECT COUNT(*) FROM admins WHERE username = ?', (username,))
        return cursor.fetchone()[0] > 0

    @staticmethod
    def is_password_strong(password):
        return True, "Password is strong enough."

    def register_admin(self, current_user, username, password1, password2, role='admin'):
        if not current_user:
            return False, 'Пользователь не авторизован!'
        if not self.is_super_admin(current_user):
            return False, 'Только супер-администраторы могут выполнять это действие!'
        with self.get_connection() as connection:
            cursor = connection.cursor()

            if self.is_admin_exist(username, cursor):
                return False, 'Имя пользователя занято!'
            if password1 != password2:
                return False, 'Пароли не совпадают'

            is_strong, message = self.is_password_strong(password1)
            if not is_strong:
                return False, message

            admin = Admin(username=username, password=password1)
            cursor.execute(
                'INSERT INTO admins (username, password, role) VALUES (?, ?, ?)',
                (admin.username, admin.hashed_password, role)
            )
            connection.commit()
            return True, 'Администратор успешно зарегистрирован!'

    def login_admin(self, username, password):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT password FROM admins WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result is None:
                return False, 'Пользователь не найден!'
            stored_password = result[0]
            if Admin.check_password(stored_password, password) is False:
                return False, 'Неверный пароль!'
            return True, 'Вход выполнен успешено!'

    def is_super_admin(self, username):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT role FROM admins WHERE username = ?', (username,))
            result = cursor.fetchone()
            return result and result[0] == 'super_admin'

    def is_admin(self, username):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT role FROM admins WHERE username = ?", (username,))
            user_role = cursor.fetchone()
            return user_role and (user_role[0] == 'admin' or user_role[0] == 'super_admin')

    def delete_admin(self, current_user, username):
        if not self.is_super_admin(current_user):
            if not current_user:
                return False, 'Пользователь не авторизован!'
            return False, 'Только супер-администраторы могут выполнять это действие!'
        with self.get_connection() as connection:
            cursor = connection.cursor()
            if not self.is_admin_exist(username, cursor):
                return False, 'Администратор не найден!'
            cursor.execute('SELECT role FROM admins WHERE username = ?', (username,))
            role = cursor.fetchone()
            if role and role[0] == 'super_admin':
                return False, 'Нельзя удалить супер-администратора!'
        cursor.execute('DELETE FROM admins WHERE username = ?', (username,))
        connection.commit()
        return True, 'Администратор успешно удален!'

    def get_all_admins(self, current_user):
        if not current_user:
            return False, 'Пользователь не авторизован!'

        if not self.is_super_admin(current_user):
            return False, 'Только супер-администраторы могут просматривать список администраторов!'

        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT username, role FROM admins WHERE role IN (?, ?)',
                           ('admin', 'super_admin'))
            admins = cursor.fetchall()
        return True, [{"username": row[0], "role": row[1]} for row in admins]

    def change_password(self, username, current_password, new_password1, new_password2):
        with self.get_connection() as connection:
            cursor = connection.cursor()

            if not self.is_admin_exist(username, cursor):
                return False, 'Пользователь не найден!'

            cursor.execute('SELECT password FROM admins WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result is None:
                return False, 'Пользователь не найден!'
            stored_password = result[0]

            if not Admin.check_password(stored_password, current_password):
                return False, 'Текущий пароль неверен!'

            if new_password1 != new_password2:
                return False, 'Новые пароли не совпадают!'

            is_strong, message = self.is_password_strong(new_password1)
            if not is_strong:
                return False, message

            new_hashed_password = Admin.hash_password(new_password1)
            cursor.execute('UPDATE admins SET password = ? WHERE username = ?',
                           (new_hashed_password, username))
            connection.commit()

            return True, 'Пароль успешно изменён!'

    def promote_to_super_admin(self, current_user, username):
        if not current_user:
            return False, 'Пользователь не авторизован!'

        if not self.is_super_admin(current_user):
            return False, 'Только супер-администраторы могут выполнять это действие!'

        with self.get_connection() as connection:
            cursor = connection.cursor()

            if not self.is_admin_exist(username, cursor):
                return False, 'Администратор не найден!'

            cursor.execute('UPDATE admins SET role = ? WHERE username = ?', ('admin', current_user))

            cursor.execute('UPDATE admins SET role = ? WHERE username = ?', ('super_admin', username))
            connection.commit()

        return True, f'Администратор {username} успешно переназначен на супер-администратора!'
