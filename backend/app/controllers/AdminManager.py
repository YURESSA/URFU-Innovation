from sqlalchemy import select

from app.database import SessionLocal
from app.models.admin import Admin


class AdminManager:
    def __init__(self, session_factory=None):
        self.session_factory = session_factory or SessionLocal

    @staticmethod
    def is_password_strong(password):
        return True, "Password is strong enough."

    @staticmethod
    def is_admin_exist(session, username):
        return session.get(Admin, username) is not None

    def is_super_admin(self, username):
        with self.session_factory() as session:
            admin = session.get(Admin, username)
            return admin is not None and admin.role == "super_admin"

    def is_admin(self, username):
        with self.session_factory() as session:
            admin = session.get(Admin, username)
            return admin is not None and admin.role in ("admin", "super_admin")

    def register_admin(self, current_user, username, password1, password2, role="admin"):
        if not current_user:
            return False, "Пользователь не авторизован!"

        if not self.is_super_admin(current_user):
            return False, "Только супер-администраторы могут выполнять это действие!"

        if password1 != password2:
            return False, "Пароли не совпадают!"

        is_strong, message = self.is_password_strong(password1)
        if not is_strong:
            return False, message

        with self.session_factory() as session:
            if self.is_admin_exist(session, username):
                return False, "Имя пользователя занято!"

            admin = Admin(
                username=username,
                password=Admin.hash_password(password1),
                role=role
            )
            session.add(admin)
            session.commit()

        return True, "Администратор успешно зарегистрирован!"

    def login_admin(self, username, password):
        with self.session_factory() as session:
            admin = session.get(Admin, username)

            if not admin:
                return False, "Пользователь не найден!"

            if not Admin.check_password(admin.password, password):
                return False, "Неверный пароль!"

            return True, "Вход выполнен успешно!"

    def delete_admin(self, current_user, username):
        if not current_user:
            return False, "Пользователь не авторизован!"

        if not self.is_super_admin(current_user):
            return False, "Только супер-администраторы могут выполнять это действие!"

        with self.session_factory() as session:
            admin = session.query(Admin).filter_by(username=username).first()

            if not admin:
                return False, "Администратор не найден!"

            if admin.role == "super_admin":
                return False, "Нельзя удалить супер-администратора!"

            session.delete(admin)
            session.commit()

        return True, "Администратор успешно удален!"

    def get_all_admins(self, current_user):
        if not current_user:
            return False, "Пользователь не авторизован!"

        if not self.is_super_admin(current_user):
            return False, "Только супер-администраторы могут просматривать список администраторов!"

        with self.session_factory() as session:
            admins = session.scalars(
                select(Admin).where(Admin.role.in_(("admin", "super_admin")))
            ).all()

            return True, [
                {"username": admin.username, "role": admin.role}
                for admin in admins
            ]

    def change_password(self, username, current_password, new_password1, new_password2):
        if new_password1 != new_password2:
            return False, "Новые пароли не совпадают!"

        is_strong, message = self.is_password_strong(new_password1)
        if not is_strong:
            return False, message

        with self.session_factory() as session:
            admin = session.get(Admin, username)

            if not admin:
                return False, "Пользователь не найден!"

            if not Admin.check_password(admin.password, current_password):
                return False, "Текущий пароль неверен!"

            admin.password = Admin.hash_password(new_password1)
            session.commit()

        return True, "Пароль успешно изменён!"

    def promote_to_super_admin(self, current_user, username):
        if not current_user:
            return False, "Пользователь не авторизован!"

        if not self.is_super_admin(current_user):
            return False, "Только супер-администраторы могут выполнять это действие!"

        with self.session_factory() as session:
            target = session.get(Admin, username)
            current = session.get(Admin, current_user)

            if not target:
                return False, "Администратор не найден!"

            current.role = "admin"
            target.role = "super_admin"

            session.commit()

        return True, f"Администратор {username} успешно переназначен на супер-администратора!"
