from flask import request, session, jsonify


def process_post_request(user_manager, test_manager, flask_session):
    data = request.json
    telegram_id = session.get('telegram_id')
    if not telegram_id:
        return jsonify(
            {"success": False, "message": "Пользователь не авторизован!"}), 401

    user_id = user_manager.get_user_id(telegram_id)
    test_id = 1
    user_test_id = user_manager.add_test_to_user(user_id, test_id)

    result = calculate_section_scores(data)

    roles_data = test_manager.get_roles_and_descriptions()
    data_percentages = calculate_percentages(result)
    data_percentages = dict(sorted(data_percentages.items(), key=lambda item: item[1], reverse=True))
    top_result, bottom_result = get_tops_and_bottoms_sections(data_percentages)
    built_top_result = build_top_result(top_result, roles_data)
    built_bottom_result = build_bottom_result(bottom_result, roles_data)
    test_manager.save_user_answers(user_test_id, result)
    data_roles = {roles_data.get(k).get('role_in_team'): v for k, v in data_percentages.items()}


    return jsonify({
        "success": True,
        "message": "Форма успешно принята",
        "prefer_roles": built_top_result,
        "un_prefer_roles": built_bottom_result,
        "all_roles": data_roles
    }), 200


def get_questions(test_manager):
    questions = test_manager.get_all_questions()
    return jsonify({"success": True, "questions": questions}), 200


def calculate_section_scores(data):
    return {
        'section1': data[2][0] + data[1][1] + data[5][2] + data[0][3] + data[4][5] + data[6][6] + data[3][7],
        'section2': data[6][0] + data[3][1] + data[2][2] + data[4][3] + data[1][4] + data[0][5] + data[5][6],
        'section3': data[5][0] + data[0][2] + data[2][3] + data[3][4] + data[6][5] + data[1][6] + data[4][7],
        'section4': data[4][0] + data[6][1] + data[3][2] + data[1][3] + data[5][4] + data[2][6] + data[0][7],
        'section5': data[1][0] + data[4][1] + data[3][3] + data[6][4] + data[5][5] + data[0][6] + data[2][7],
        'section6': data[3][0] + data[0][1] + data[5][1] + data[4][2] + data[2][4] + data[1][5] + data[6][7],
        'section7': data[0][0] + data[1][2] + data[6][3] + data[4][4] + data[2][5] + data[3][6] + data[5][7],
        'section8': data[2][1] + data[6][2] + data[5][3] + data[0][4] + data[3][5] + data[4][6] + data[1][7],
    }


def calculate_percentages(result):
    total_sum = sum(result.values())
    return {key: round((value / total_sum) * 100) for key, value in result.items()}


def get_tops_and_bottoms_sections(data_percentages):
    filtered_data = {key: value for key, value in data_percentages.items() if value > 0}
    sorted_values = sorted(set(filtered_data.values()), reverse=True)
    top_two_values = set(sorted_values[:2])
    top_result = {key: value for key, value in filtered_data.items() if value in top_two_values}

    if len(top_result) < 3:
        top_two_values = set(sorted_values[:3])
        top_result = {key: value for key, value in filtered_data.items() if value in top_two_values}

    filtered_data = {key: value for key, value in data_percentages.items() if key not in top_result.keys()}
    sorted_values_bottom = sorted(set(filtered_data.values()))
    bottom_two_values = set(sorted_values_bottom[:2])
    bottom_result = {key: value for key, value in filtered_data.items() if
                     value in bottom_two_values and key not in top_result}

    if len(bottom_result) < 3:
        bottom_two_values = set(sorted_values_bottom[:3])
        bottom_result = {key: value for key, value in filtered_data.items() if
                         value in bottom_two_values and key not in top_result}
    return top_result, bottom_result


def build_top_result(final_data, roles_data):
    final_result = []
    for section, value in final_data.items():
        role_info = roles_data.get(section)
        if role_info:
            final_result.append({
                'role': role_info['role_in_team'],
                'strong_side': role_info['strong-side'],
                'weak_side': role_info['weak-side'],
                'value': value,
                'term': role_info['term'],
                'goal': role_info['goal'],
                'description': role_info['description'],
                'file_name': role_info['file_name']
            })
    return final_result


def build_bottom_result(final_data, roles_data):
    final_result = []
    for section, value in final_data.items():
        role_info = roles_data.get(section)
        if role_info:
            final_result.append({
                'role': role_info['role_in_team'],
                'value': value,
                'weak_side': role_info['weak-side'],
                'strong_side': role_info['strong-side'],
                'term': role_info['term'],
                'goal': role_info['goal'],
                'recommendations': role_info['recommendations'],
                'description': role_info['description'],
                'file_name': role_info['file_name']
            })
    return final_result
