from flask import Flask, request, jsonify, session
from flask_cors import CORS

from controllers.AdminManager import AdminManager
from controllers.DatabaseController import DatabaseController
from controllers.UserManager import UserManager

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
app.secret_key = 'URFU-INNOVATE-2024'
admin_manager = AdminManager()
user_manager = UserManager()
db_controller = DatabaseController()


@app.route('/api/register-user', methods=['POST'])
def register_user():
    data = request.form
    full_name = data.get('full_name')
    phone_number = data.get('phone_number')
    telegram_id = data.get('telegram_id')
    if not all([full_name, phone_number, telegram_id]):
        return jsonify({"success": False, "message": "Необходимо заполнить все поля"}), 400

    is_success, message = user_manager.register_user(full_name, phone_number, telegram_id)
    session['telegram_id'] = telegram_id
    code = 201

    return jsonify({"telegram_id": telegram_id, "success": is_success, "message": 'Форма успешно принята'}), code


@app.route('/api/get-test-results', methods=['GET'])
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


@app.route('/api/get-all-test', methods=['GET'])
def get_all_test():
    tests = db_controller.get_tests()
    corr_tests = []
    for test in tests:
        corr_test = {'test_title': test[0], 'test_url': test[1]}
        corr_tests.append(corr_test)
    return jsonify(corr_tests)


def get_top_sections(section_data):
    sorted_sections = sorted(section_data.items(), key=lambda x: x[1], reverse=True)
    top_values = [sorted_sections[0][1], sorted_sections[1][1], sorted_sections[2][1]]

    if len(set(top_values)) == 3:
        return [sorted_sections[0][0], sorted_sections[1][0]]
    else:
        return [sorted_sections[0][0], sorted_sections[1][0], sorted_sections[2][0]]


@app.route('/api/belbin-test', methods=['GET', 'POST'])
def processing_form():
    if request.method == 'POST':
        return process_post_request()

    if request.method == 'GET':
        return get_questions()


def process_post_request():
    data = request.json
    telegram_id = list(data.keys())[0]
    data = data.get(telegram_id)
    print(telegram_id)
    if not telegram_id:
        return jsonify({"success": False, "message": "Пользователь не авторизован!"}), 401

    user_id = user_manager.get_user_id(telegram_id)[0]
    test_id = 1
    user_test_id = user_manager.add_test_to_user(user_id, test_id)

    data = {key: int(value) for key, value in data.items()}
    print(data)
    result = calculate_section_scores(data)

    roles_data = db_controller.get_roles_and_descriptions()
    data_percentages = calculate_percentages(result)

    final_data = get_top_two_sections(data_percentages)
    final_result = build_final_result(final_data, roles_data)

    db_controller.save_user_answers(user_test_id, data_percentages)
    data_roles = {roles_data.get(k).get('role_in_team'): v for k, v in data_percentages.items()}

    logout_user()

    return jsonify({
        "success": True,
        "message": "Форма успешно принята",
        "prefer_roles": final_result,
        "all_roles": data_roles
    }), 200


def get_questions():
    questions = db_controller.get_all_questions()
    return jsonify({"success": True, "questions": questions}), 200


def calculate_section_scores(data):
    return {
        'section1': data.get('3section1') + data.get('2section2') + data.get('6section3') + data.get('1section4') +
                    data.get('5section6') + data.get('7section7') + data.get('4section8'),
        'section2': data.get('7section1') + data.get('4section2') + data.get('3section3') + data.get('5section4') +
                    data.get('2section5') + data.get('1section6') + data.get('6section7'),
        'section3': data.get('6section1') + data.get('1section3') + data.get('3section4') + data.get('4section5') +
                    data.get('7section6') + data.get('2section7') + data.get('5section8'),
        'section4': data.get('5section1') + data.get('7section2') + data.get('4section3') + data.get('2section4') +
                    data.get('6section5') + data.get('3section7') + data.get('1section8'),
        'section5': data.get('2section1') + data.get('5section2') + data.get('4section4') + data.get('7section5') +
                    data.get('6section6') + data.get('1section7') + data.get('3section8'),
        'section6': data.get('4section1') + data.get('1section2') + data.get('6section2') + data.get('5section3') +
                    data.get('3section5') + data.get('2section6') + data.get('7section8'),
        'section7': data.get('1section1') + data.get('2section3') + data.get('7section4') + data.get('5section5') +
                    data.get('3section6') + data.get('4section7') + data.get('6section8'),
        'section8': data.get('3section2') + data.get('7section3') + data.get('6section4') + data.get('1section5') +
                    data.get('4section6') + data.get('5section7') + data.get('2section8'),
    }


def calculate_percentages(result):
    total_sum = sum(result.values())
    return {key: round((value / total_sum) * 100) for key, value in result.items()}


def get_top_two_sections(data_percentages):
    sorted_values = sorted(set(data_percentages.values()), reverse=True)[:2]
    top_two_values = set(sorted_values)
    return {key: value for key, value in data_percentages.items() if value in top_two_values}


def build_final_result(final_data, roles_data):
    final_result = []
    for section, value in final_data.items():
        role_info = roles_data.get(section)
        if role_info:
            final_result.append({
                'role': role_info['role_in_team'],
                'value': value,
                'description': role_info['description']
            })
    return final_result


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


@app.route('/api/change-password', methods=['POST'])
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


@app.route('/api/delete-admin', methods=['DELETE'])
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


@app.route('/api/promote-to-super-admin', methods=['POST'])
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
