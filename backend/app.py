from flask import Flask, request, jsonify, session

from controllers.AdminManager import AdminManager
from controllers.UserManager import UserManager

app = Flask(__name__)
app.secret_key = 'URFU-INNOVATE-2024'
admin_manager = AdminManager()
user_manager = UserManager()


@app.route('/api/register-user', methods=['POST'])
def register_user():
    """Обработка регистрации нового пользователя"""
    data = request.form
    full_name = data.get('full_name')
    phone_number = data.get('phone_number')
    telegram_id = data.get('telegram_id')

    # Проверка, что все поля заполнены
    if not all([full_name, phone_number, telegram_id]):
        return jsonify({"success": False, "message": "Необходимо заполнить все поля"}), 400

    is_success, message = user_manager.register_user(full_name, phone_number, telegram_id)
    session['telegram_id'] = telegram_id
    code = 201

    return jsonify({"success": is_success, "message": 'Форма успешно принята'}), code


@app.route('/api/get_test_results', methods=['POST'])
def get_test_results():
    data = request.form
    telegram_id = data.get('telegram_id')
    test_name = data.get('test_name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    current_user = session.get('username')
    if not current_user or not admin_manager.is_admin(current_user):
        return jsonify({"success": False, "message": "Только администратторы могут выполнять данное действие!"}), 403

    results = admin_manager.get_filtered_results(telegram_id, test_name, start_date, end_date)
    return jsonify({"success": True, "results": results}), 200


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


@app.route('/api/logout-user', methods=['POST'])
def logout_user():
    session.pop('telegram_id', None)
    return jsonify({"success": True, "message": 'Вы успешно вышли'}), 200


def get_top_sections(section_data):
    sorted_sections = sorted(section_data.items(), key=lambda x: x[1], reverse=True)
    top_values = [sorted_sections[0][1], sorted_sections[1][1], sorted_sections[2][1]]

    if len(set(top_values)) == 3:
        return [sorted_sections[0][0], sorted_sections[1][0]]
    else:
        return [sorted_sections[0][0], sorted_sections[1][0], sorted_sections[2][0]]


def convert_sections_to_roles(section_names):
    section_role = {'section1': 'Формальный лидер',
                    'section2': 'Неформальный лидер',
                    'section3': 'Генератор идей',
                    'section4': 'Критик',
                    'section5': 'Организатор работ',
                    'section6': 'Организатор группы',
                    'section7': 'Разведчик',
                    'section8': 'Контролер'
                    }
    roles = [section_role.get(section) for section in section_names if section in section_role]
    return roles


@app.route('/api/belbin_test', methods=['POST'])
def processing_form():
    data = request.form
    telegram_id = session.get('telegram_id')
    if not telegram_id:
        return jsonify({"success": False, "message": "Пользователь не авторизован!"}), 401

    user_id = user_manager.get_user_id(telegram_id)[0]
    test_id = 1
    user_test_id = user_manager.add_test_to_user(user_id, test_id)

    section_data = {}
    for key in list(data):
        section_data[key] = round(int(data[key]) / 70 * 100)
    print(section_data)
    top_sections = get_top_sections(section_data)
    roles = convert_sections_to_roles(top_sections)
    user_manager.save_user_answers(user_test_id, section_data)
    logout_user()
    return jsonify({"success": True, "message": "Форма успешно принята", "roles": roles}), 200


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


@app.route('/api/promote_to_super_admin', methods=['POST'])
def promote_to_super_admin():
    current_user = session.get('username')
    if not current_user:
        return jsonify({"success": False, "message": "Пользователь не авторизован!"}), 401

    data = request.form
    username = data.get('username')

    is_success, message = admin_manager.promote_to_super_admin(current_user, username)
    code = 200 if is_success else 403
    return jsonify({"success": is_success, "message": message}), code


if __name__ == "__main__":
    app.run()
