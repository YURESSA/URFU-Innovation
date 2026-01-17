import json
import os
from datetime import datetime

from app.models.user_test import UserTest
from app.models.user_test_result import UserTestResult

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DISC_TEST_PATH = os.path.join(
    BASE_DIR,
    '..',
    'data',
    'disc',
    'disc.json'
)


def get_disc_test_questions():
    with open(DISC_TEST_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


DISC_KEY = {
    "D": [(1, "B"), (2, "C"), (3, "D"), (4, "A"), (5, "C"), (6, "C"), (7, "B"), (8, "B"), (9, "A"), (10, "A"),
          (11, "B"), (12, "D"), (13, "B"), (14, "B"), (15, "A")],
    "I": [(1, "A"), (2, "B"), (3, "B"), (4, "C"), (5, "B"), (6, "A"), (7, "B"), (8, "C"), (9, "D"), (10, "B"),
          (11, "C"), (12, "A"), (13, "A"), (14, "C"), (15, "B")],
    "S": [(1, "C"), (2, "A"), (3, "C"), (4, "D"), (5, "A"), (6, "D"), (7, "A"), (8, "A"), (9, "B"), (10, "B"),
          (11, "D"), (12, "B"), (13, "C"), (14, "D"), (15, "C")],
    "C": [(1, "D"), (2, "D"), (3, "A"), (4, "B"), (5, "D"), (6, "B"), (7, "A"), (8, "D"), (9, "C"), (10, "A"),
          (11, "A"), (12, "C"), (13, "D"), (14, "A"), (15, "D")]
}


def calculate_disc_scores(data):
    answers = {item["question_id"]: item["answer"] for item in data["answers"]}

    scores = {"D": 0, "I": 0, "S": 0, "C": 0}

    for disc_type, mapping in DISC_KEY.items():
        for q_id, correct_answer in mapping:
            if answers.get(q_id) == correct_answer:
                scores[disc_type] += 1

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    primary = sorted_scores[0][0]
    secondary = sorted_scores[1][0] if sorted_scores[1][1] >= sorted_scores[0][1] - 2 else None

    return {
        "scores": scores,
        "primary": primary,
        "secondary": secondary
    }


def save_disc_test_results(db, user_id, test_id, scores: dict):
    user_test = db.query(UserTest).filter_by(
        user_id=user_id,
        test_id=test_id
    ).first()

    if user_test:
        user_test.timestamp = datetime.now()
    else:
        user_test = UserTest(
            user_id=user_id,
            test_id=test_id
        )
        db.add(user_test)
        db.flush()

    for scale, value in scores.items():
        result = db.query(UserTestResult).filter_by(
            user_test_id=user_test.user_test_id,
            scale=scale
        ).first()
        if result:
            result.value = value
        else:
            db.add(UserTestResult(
                user_test_id=user_test.user_test_id,
                scale=scale,
                value=value
            ))

    db.commit()
    return user_test
