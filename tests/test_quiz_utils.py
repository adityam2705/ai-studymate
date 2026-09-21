import json

import pytest

from utils.quiz_utils import QuizValidationError, calculate_score, parse_quiz_response


def valid_payload():
    return {
        "questions": [
            {
                "question": "What is a process?",
                "options": {"A": "A running program", "B": "A disk", "C": "A mouse", "D": "A cable"},
                "correct_answer": "A",
                "explanation": "A process is a program in execution.",
            }
        ]
    }


def test_parse_quiz_response_accepts_valid_json():
    questions = parse_quiz_response(json.dumps(valid_payload()), 1)
    assert questions[0]["correct_answer"] == "A"


def test_parse_quiz_response_rejects_invalid_json():
    with pytest.raises(QuizValidationError, match="unexpected format"):
        parse_quiz_response("not JSON", 1)


def test_parse_quiz_response_rejects_wrong_option_labels():
    payload = valid_payload()
    payload["questions"][0]["options"] = {"A": "one", "B": "two", "C": "three"}
    with pytest.raises(QuizValidationError, match="four options"):
        parse_quiz_response(json.dumps(payload), 1)


def test_calculate_score_returns_feedback():
    questions = parse_quiz_response(json.dumps(valid_payload()), 1)
    score, feedback = calculate_score(questions, {0: "B"})
    assert score == 0
    assert feedback[0]["is_correct"] is False
    assert feedback[0]["correct_answer"] == "A"
