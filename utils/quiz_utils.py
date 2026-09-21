"""Parse, validate, and score the structured quiz returned by Gemini."""

from __future__ import annotations

import json
from typing import Any


class QuizValidationError(ValueError):
    """Raised when AI output is not a safe, displayable quiz."""


def _remove_markdown_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


def parse_quiz_response(response_text: str, expected_count: int) -> list[dict[str, Any]]:
    """Convert JSON text into validated questions with A-D answer labels."""
    if not response_text or not response_text.strip():
        raise QuizValidationError("The AI returned an empty quiz. Please try again.")

    try:
        payload = json.loads(_remove_markdown_fences(response_text))
    except json.JSONDecodeError as error:
        raise QuizValidationError(
            "The AI returned quiz data in an unexpected format. Please generate it again."
        ) from error

    questions = payload.get("questions") if isinstance(payload, dict) else payload
    if not isinstance(questions, list) or len(questions) != expected_count:
        raise QuizValidationError(
            f"The quiz must contain exactly {expected_count} questions. Please try again."
        )

    validated_questions = []
    for number, item in enumerate(questions, start=1):
        if not isinstance(item, dict):
            raise QuizValidationError(f"Question {number} is not in the expected format.")

        question = item.get("question")
        options = item.get("options")
        correct_answer = item.get("correct_answer")
        explanation = item.get("explanation")

        if not isinstance(question, str) or not question.strip():
            raise QuizValidationError(f"Question {number} is missing its question text.")
        if not isinstance(options, dict) or set(options) != {"A", "B", "C", "D"}:
            raise QuizValidationError(
                f"Question {number} must have exactly four options labelled A to D."
            )
        if not all(isinstance(value, str) and value.strip() for value in options.values()):
            raise QuizValidationError(f"Question {number} contains an empty option.")
        if correct_answer not in options:
            raise QuizValidationError(f"Question {number} has an invalid correct answer.")
        if not isinstance(explanation, str) or not explanation.strip():
            raise QuizValidationError(f"Question {number} is missing its explanation.")

        validated_questions.append(
            {
                "question": question.strip(),
                "options": {key: value.strip() for key, value in options.items()},
                "correct_answer": correct_answer,
                "explanation": explanation.strip(),
            }
        )
    return validated_questions


def calculate_score(
    questions: list[dict[str, Any]], answers: dict[int, str]
) -> tuple[int, list[dict[str, Any]]]:
    """Return the score and per-question feedback after a student submits."""
    feedback = []
    score = 0
    for index, question in enumerate(questions):
        selected_answer = answers.get(index)
        is_correct = selected_answer == question["correct_answer"]
        score += int(is_correct)
        feedback.append(
            {
                "selected_answer": selected_answer,
                "correct_answer": question["correct_answer"],
                "is_correct": is_correct,
                "explanation": question["explanation"],
            }
        )
    return score, feedback
