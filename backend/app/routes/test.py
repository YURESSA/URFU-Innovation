from flask import Blueprint, request, session, jsonify
from ..controllers.TestManager import TestManager
from ..controllers.UserManager import UserManager
from ..services.belbin_service import process_post_request, get_questions
from ..services.excel_service import create_excel_file, adjust_column_widths, save_and_send_file
from ..database import SessionLocal
from ..paths import BELBIN_TEST_PATH
from flask import session as flask_session
test_bp = Blueprint('test', __name__)
user_manager = UserManager(session_factory=SessionLocal)
test_manager = TestManager(session_factory=SessionLocal, belbin_test=BELBIN_TEST_PATH)

@test_bp.route('/get-all-test', methods=['GET'])
def get_all_test():
    tests = test_manager.get_tests()
    return jsonify([{'test_title': t[0], 'test_url': t[1]} for t in tests])

@test_bp.route('/belbin-test', methods=['GET', 'POST'])
def processing_form():
    if request.method == 'POST':
        return process_post_request(user_manager, test_manager, flask_session)
    return get_questions(test_manager)

@test_bp.route('/get-test-results', methods=['GET'])
def get_test_results():
    data = request.form
    telegram_id = data.get('telegram_id')
    test_name = data.get('test_name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    current_user = session.get('admin_username')
    from ..controllers.AdminManager import AdminManager
    admin_manager = AdminManager(SessionLocal)
    if not current_user or not admin_manager.is_admin(current_user):
        return jsonify({"success": False, "message": "Только администраторы могут выполнять данное действие!"}), 403

    results = test_manager.get_filtered_results(telegram_id, test_name, start_date, end_date)
    return jsonify({"success": True, "results": results}), 200

@test_bp.route('/save-test-results', methods=['GET'])
def save_test_results():
    data = request.form
    telegram_id = data.get('telegram_id')
    test_name = data.get('test_name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    current_user = session.get('admin_username')
    from ..controllers.AdminManager import AdminManager
    admin_manager = AdminManager(SessionLocal)
    if not current_user or not admin_manager.is_admin(current_user):
        return jsonify({"success": False, "message": "Только администраторы могут выполнять данное действие!"}), 403

    results = test_manager.get_filtered_results(telegram_id, test_name, start_date, end_date)
    wb, ws = create_excel_file(results)
    adjust_column_widths(ws)
    return save_and_send_file(wb)
