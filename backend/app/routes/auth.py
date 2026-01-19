from flask import Blueprint, request, session, jsonify
from sqlalchemy.orm import joinedload

from ..controllers.UserManager import UserManager
from ..database import SessionLocal
from ..models.user_test import UserTest
from ..services.belbin_service import build_top_result, build_bottom_result, get_tops_and_bottoms_sections, \
    calculate_percentages

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager(session_factory=SessionLocal)


@auth_bp.route('/register-user', methods=['POST'])
def register_user():
    data = request.form
    full_name = data.get('full_name')
    phone_number = data.get('phone_number')
    telegram_id = data.get('telegram_id')
    password = data.get('password')

    if not all([full_name, phone_number, telegram_id, password]):
        return jsonify({"success": False, "message": "Необходимо заполнить все поля"}), 400

    from ..controllers.UserManager import UserManager
    user_manager = UserManager(SessionLocal)
    is_success, message = user_manager.register_user(full_name, phone_number, telegram_id, password)

    if is_success:
        session['telegram_id'] = telegram_id

    return jsonify({"success": is_success, "message": message}), 201


@auth_bp.route('/login-user', methods=['POST'])
def login_user():
    data = request.form
    telegram_id = data.get('telegram_id')
    password = data.get('password')

    if not all([telegram_id, password]):
        return jsonify({"success": False, "message": "Необходимо указать Telegram ID и пароль"}), 400

    from ..controllers.UserManager import UserManager
    from ..controllers.TestManager import TestManager

    user_manager = UserManager(SessionLocal)
    test_manager = TestManager(SessionLocal)

    user = user_manager.get_user_by_telegram(telegram_id)
    if not user or not user.check_password(password):
        return jsonify({"success": False, "message": "Неверный Telegram ID или пароль"}), 401

    session['telegram_id'] = telegram_id

    roles_dict = test_manager.get_roles_and_descriptions()
    roles = [v["role_in_team"] for v in roles_dict.values()]

    user_tests = []
    with SessionLocal() as db_session:
        tests = db_session.query(UserTest).options(
            joinedload(UserTest.results),
            joinedload(UserTest.answers)
        ).filter(UserTest.user_id == user.user_id).order_by(UserTest.timestamp.desc()).all()

        for ut in tests:
            test_data = {
                "user_test_id": str(ut.user_test_id),  # добавляем test_id
                "test_name": getattr(ut.test_id, "display_name", str(ut.test_id)),
                "timestamp": ut.timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "sections": {}
            }

            if hasattr(ut, "results") and ut.results:
                test_data["sections"] = {r.scale: r.value for r in ut.results}

            elif hasattr(ut, "answers") and ut.answers:
                test_data["sections"] = {role: getattr(ut.answers, f"section{i + 1}")
                                         for i, role in enumerate(roles)}

            user_tests.append(test_data)

    return jsonify({
        "success": True,
        "message": "Вы успешно вошли",
        "user": {
            "full_name": user.full_name,
            "phone_number": user.phone_number,
            "telegram_id": user.telegram_id,
            "tests": user_tests
        }
    }), 200


@auth_bp.route('/logout-user', methods=['POST'])
def logout_user():
    session.pop('telegram_id', None)
    return jsonify({"success": True, "message": 'Вы успешно вышли'}), 200


@auth_bp.route('/user-test/<int:user_test_id>', methods=['GET'])
def get_user_test(user_test_id):
    telegram_id = session.get('telegram_id')
    if not telegram_id:
        return jsonify({"success": False, "message": "Пользователь не авторизован"}), 401

    from ..controllers.UserManager import UserManager
    from ..controllers.TestManager import TestManager
    from app.models.user_test import UserTest
    from sqlalchemy.orm import joinedload

    user_manager = UserManager(SessionLocal)
    test_manager = TestManager(SessionLocal)

    user = user_manager.get_user_by_telegram(telegram_id)
    if not user:
        return jsonify({"success": False, "message": "Пользователь не найден"}), 404

    roles_data = test_manager.get_roles_and_descriptions()

    with SessionLocal() as db_session:
        ut = db_session.query(UserTest).options(
            joinedload(UserTest.answers)
        ).filter(
            UserTest.user_test_id == user_test_id,
            UserTest.user_id == user.user_id
        ).first()

        if not ut:
            return jsonify({
                "success": False,
                "message": "Тест не найден или не принадлежит пользователю"
            }), 404

        if not ut.answers:
            return jsonify({"success": False, "message": "Результаты BELBIN не найдены"}), 404

        sections = {
            f"section{i}": getattr(ut.answers, f"section{i}")
            for i in range(1, 9)
        }

        data_percentages = calculate_percentages(sections)
        data_percentages = dict(
            sorted(data_percentages.items(), key=lambda item: item[1], reverse=True)
        )

        top_result, bottom_result = get_tops_and_bottoms_sections(data_percentages)

        built_top_result = build_top_result(top_result, roles_data)
        built_bottom_result = build_bottom_result(bottom_result, roles_data)

        all_roles = {
            roles_data[k]["role_in_team"]: v
            for k, v in data_percentages.items()
        }

    return jsonify({
        "success": True,
        "test": {
            "user_test_id": ut.user_test_id,
            "test_id": str(ut.test_id),
            "test_name": getattr(ut.test_id, "display_name", str(ut.test_id)),
            "timestamp": ut.timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "prefer_roles": built_top_result,
            "un_prefer_roles": built_bottom_result,
            "all_roles": all_roles
        }
    }), 200
