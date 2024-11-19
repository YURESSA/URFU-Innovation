import bcrypt
from flask_login import UserMixin


class Admin(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.hashed_password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def check_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    def get_id(self):
        return self.username
