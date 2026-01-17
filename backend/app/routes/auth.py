from flask import Blueprint, request, session, jsonify
from ..controllers.UserManager import UserManager
from ..database import SessionLocal

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager(session_factory=SessionLocal)

@auth_bp.route('/register-user', methods=['POST'])
def register_user():
    data = request.form
    full_name = data.get('full_name')
    phone_number = data.get('phone_number')
    telegram_id = data.get('telegram_id')
    if not all([full_name, phone_number, telegram_id]):
        return jsonify({"success": False, "message": "Необходимо заполнить все поля"}), 400

    is_success, message = user_manager.register_user(full_name, phone_number, telegram_id)
    session['telegram_id'] = telegram_id
    return jsonify({"success": is_success, "message": 'Форма успешно принята'}), 201

@auth_bp.route('/logout-user', methods=['POST'])
def logout_user():
    session.pop('telegram_id', None)
    return jsonify({"success": True, "message": 'Вы успешно вышли'}), 200