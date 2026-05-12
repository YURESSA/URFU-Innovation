from flask import Blueprint, request, session, jsonify
from ..controllers.AdminManager import AdminManager
from ..controllers.UserManager import UserManager
from ..database import SessionLocal
from ..services.excel_service import create_bitrix_users_excel, send_workbook

admin_bp = Blueprint('admin', __name__)
admin_manager = AdminManager(session_factory=SessionLocal)
user_manager = UserManager(session_factory=SessionLocal)

@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    is_success, message = admin_manager.login_admin(username, password)
    if not is_success:
        return jsonify({"success": False, "message": message}), 401
    session['admin_username'] = username
    role = admin_manager.is_super_admin(username)
    return jsonify({"success": is_success, "message": message, "super_admin": role}), 200

@admin_bp.route('/logout', methods=['GET'])
def logout():
    session.pop('admin_username', None)
    return jsonify({"success": True, "message": 'Вы успешно вышли'}), 200

@admin_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    current_user = session.get('admin_username')
    if not current_user:
        return jsonify({"success": False, "message": "Пользователь не авторизован!"}), 401

    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')

    is_success, message = admin_manager.register_admin(current_user, username, password1, password2)
    code = 201 if is_success else 403
    return jsonify({"success": is_success, "message": message}), code

@admin_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.form
    username = session.get('username')
    current_password = data.get('current_password')
    new_password1 = data.get('new_password1')
    new_password2 = data.get('new_password2')

    if not username:
        return jsonify({"success": False, "message": "Пользователь не авторизован!"}), 401

    is_success, message = admin_manager.change_password(username, current_password, new_password1, new_password2)
    code = 200 if is_success else 400
    return jsonify({"success": is_success, "message": message}), code

@admin_bp.route('/delete_admin', methods=['DELETE'])
def delete_admin():
    data = request.json
    print(data)
    username = data.get('username')
    current_user = session.get('admin_username')
    print(current_user, username)
    is_success, message = admin_manager.delete_admin(current_user, username)
    code = 200 if is_success else 403
    return jsonify({"success": is_success, "message": message}), code

@admin_bp.route('/admins', methods=['GET'])
def get_all_admins():
    current_user = session.get('admin_username')
    is_success, result = admin_manager.get_all_admins(current_user)
    if not is_success:
        return jsonify({"success": False, "message": result}), 403 if "Только супер-администраторы" in result else 401
    return jsonify({"success": True, "admins": result}), 200

@admin_bp.route('/promote-to-super-admin', methods=['DELETE'])
def promote_to_super_admin():
    current_user = session.get('admin_username')
    if not current_user:
        return jsonify({"success": False, "message": "Пользователь не авторизован!"}), 401

    data = request.json
    username = data.get('username')
    is_success, message = admin_manager.promote_to_super_admin(current_user, username)
    code = 200 if is_success else 403
    return jsonify({"success": is_success, "message": message}), code


def _export_bitrix_users(only_new: bool, download_name: str):
    current_user = session.get('admin_username')
    if not current_user:
        return jsonify({"success": False, "message": "Пользователь не авторизован!"}), 401

    if not admin_manager.is_admin(current_user):
        return jsonify({"success": False, "message": "Только администраторы могут выполнять данное действие!"}), 403

    users = user_manager.get_users_for_bitrix_export(only_new=only_new)
    wb, _ = create_bitrix_users_excel(users)

    user_ids = [user.user_id for user in users]
    user_manager.mark_users_as_bitrix_exported(user_ids)

    return send_workbook(wb, download_name)


@admin_bp.route('/bitrix/users/export-all', methods=['GET'])
def export_all_users_for_bitrix():
    return _export_bitrix_users(
        only_new=False,
        download_name='bitrix_users_all.xlsx'
    )


@admin_bp.route('/bitrix/users/export-new', methods=['GET'])
def export_new_users_for_bitrix():
    return _export_bitrix_users(
        only_new=True,
        download_name='bitrix_users_new.xlsx'
    )
