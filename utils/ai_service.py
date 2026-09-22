
"""Gemini calls kept separate from the Streamlit user interface."""

from __future__ import annotations

import logging
import os

import streamlit as st


class AIServiceError(RuntimeError):
    """An error that can be shown to students without exposing technical details."""


def get_api_key() -> str | None:
    """Read a key from an environment variable or Streamlit secrets."""
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if key:
        return key.strip()

    try:
        secret_key = st.secrets.get("GEMINI_API_KEY")
        return str(secret_key).strip() if secret_key else None
    except Exception:
        return None


@st.cache_resource
def _cached_client(api_key: str):
    """Create and cache one Gemini client for this API key."""
    from google import genai

    return genai.Client(api_key=api_key)


def _client():
    api_key = get_api_key()

    if not api_key:
        raise AIServiceError(
            "Gemini is not configured. Add GEMINI_API_KEY to your "
            "environment or Streamlit secrets, or turn on Demo Mode."
        )

    try:
        return _cached_client(api_key)
    except ImportError as error:
        raise AIServiceError(
            "The Gemini library is missing. Run pip install -r requirements.txt."
        ) from error


def _model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _response_text(response) -> str:
    text = getattr(response, "text", None)

    if not text or not text.strip():
        raise AIServiceError(
            "Gemini did not return usable text. The request may have been blocked "
            "or the service may be busy. Please try again."
        )

    return text.strip()


def _friendly_api_error(error: Exception) -> AIServiceError:
    message = str(error).lower()

    if any(word in message for word in (
        "api key", "401", "403", "permission"
    )):
        return AIServiceError(
            "Gemini could not verify the API key. Check your key and try again."
        )

    if any(word in message for word in (
        "429", "quota", "rate limit", "resource exhausted"
    )):
        return AIServiceError(
            "Gemini's request limit was reached. Wait a moment and try again."
        )

    if any(word in message for word in (
        "timeout", "network", "connection"
    )):
        return AIServiceError(
            "A network problem prevented Gemini from responding. "
            "Check your connection and try again."
        )

    if "client has been closed" in message:
        return AIServiceError(
            "The Gemini client was closed unexpectedly. "
            "Please reboot the app and try again."
        )

    return AIServiceError(
        "Gemini could not generate a response right now. Please try again later."
    )


def generate_summary(study_text: str, length: str) -> str:
    """Ask Gemini for student-friendly Markdown notes."""
    instructions = {
        "Short": "about 150-200 words",
        "Medium": "about 300-400 words",
        "Detailed": "about 500-700 words",
    }

    prompt = f"""You are a helpful study assistant. Summarize ONLY the study material below.
Write {instructions[length]}. Use Markdown headings and bullet points. Include important
definitions and key concepts. Use simple, accurate language for an undergraduate student.
Do not add facts that are not supported by the material.

STUDY MATERIAL:
{study_text}
"""

    try:
        response = _client().models.generate_content(
            model=_model_name(),
            contents=prompt,
        )
        return _response_text(response)

    except AIServiceError:
        raise

    except Exception as error:
        logging.exception("Gemini summary generation failed")
        raise _friendly_api_error(error) from error


def generate_quiz(study_text: str, question_count: int) -> str:
    """Ask Gemini for strict JSON so the UI can validate it before display."""
    prompt = f"""Create exactly {question_count} multiple-choice questions using ONLY the
study material below. Return valid JSON only, with no Markdown or extra text, in this form:
{{"questions": [{{"question": "...", "options": {{"A": "...", "B": "...",
"C": "...", "D": "..."}}, "correct_answer": "A", "explanation": "..."}}]}}

Each question must have four distinct, useful options, exactly one correct answer, and a
short explanation. Do not reveal answers outside the correct_answer field. Do not use
knowledge beyond the material.

STUDY MATERIAL:
{study_text}
"""

    try:
        from google.genai import types

        response = _client().models.generate_content(
            model=_model_name(),
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )

        return _response_text(response)

    except AIServiceError:
        raise

    except Exception as error:
        logging.exception("Gemini quiz generation failed")
        raise _friendly_api_error(error) from error