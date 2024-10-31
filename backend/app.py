from flask import Flask, request, jsonify, session

from controllers.AdminManager import AdminManager

app = Flask(__name__)
app.secret_key = 'URFU-INNOVATE-2024'
admin_manager = AdminManager()


@app.route('/api/register', methods=['POST'])
def register():
    data = request.form
    current_user = session.get('username')
    if not current_user:
        return jsonify({"success": False, "message": "Пользователь не авторизован!"}), 401

    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')

    is_success, message = admin_manager.register_admin(current_user, username, password1, password2)
    code = 201 if is_success else 403
    return jsonify({"success": is_success, "message": message}), code


@app.route('/api/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    is_success, message = admin_manager.login_admin(username, password)
    if not is_success:
        return jsonify({"success": False, "message": message}), 401
    session['username'] = username
    return jsonify({"success": is_success, "message": message}), 200


@app.route('/api/change_password', methods=['POST'])
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


@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"success": True, "message": 'Вы успешно вышли'}), 200


@app.route('/api/delete_admin', methods=['DELETE'])
def delete_admin():
    data = request.form
    username = data.get('username')
    current_user = session.get('username')
    is_success, message = admin_manager.delete_admin(current_user, username)
    code = 200 if is_success else 403
    return jsonify({"success": is_success, "message": message}), code


@app.route('/api/admins', methods=['GET'])
def get_all_admins():
    current_user = session.get('username')

    is_success, result = admin_manager.get_all_admins(current_user)
    if not is_success:
        return jsonify({"success": False, "message": result}), 403 if "Только супер-администраторы" in result else 401

    return jsonify({"success": True, "admins": result}), 200


if __name__ == "__main__":
    app.run()
