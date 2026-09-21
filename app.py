"""AI StudyMate - a small Streamlit study helper for an academic project."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.ai_service import AIServiceError, generate_quiz, generate_summary, get_api_key
from utils.demo_data import DEMO_QUIZ, DEMO_SUMMARY
from utils.pdf_reader import StudyTextError, extract_text_from_pdf, validate_study_text
from utils.quiz_utils import QuizValidationError, calculate_score, parse_quiz_response


PROJECT_DIR = Path(__file__).parent
SAMPLE_NOTES_PATH = PROJECT_DIR / "sample_data" / "sample_notes.txt"

st.set_page_config(page_title="AI StudyMate", page_icon="📚", layout="wide")


def read_demo_notes() -> str:
    return SAMPLE_NOTES_PATH.read_text(encoding="utf-8")


def initialise_state() -> None:
    """Create session values once so ordinary widget interactions keep results."""
    defaults = {
        "study_text": "",
        "notes_editor": "",
        "summary": "",
        "quiz": [],
        "quiz_submitted": False,
        "quiz_feedback": [],
        "quiz_score": None,
        "quiz_version": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz() -> None:
    """Clear old answers whenever a new quiz is generated."""
    st.session_state.quiz_submitted = False
    st.session_state.quiz_feedback = []
    st.session_state.quiz_score = None
    st.session_state.quiz_version += 1


def save_study_text(text: str) -> None:
    """Save validated material and remove results based on older material."""
    st.session_state.study_text = validate_study_text(text)
    st.session_state.summary = ""
    st.session_state.quiz = []
    reset_quiz()


def demo_quiz_for_count(question_count: int) -> list[dict]:
    """Use the five built-in questions; repeat no questions and explain the limit."""
    if question_count != 5:
        raise StudyTextError(
            "Demo Mode includes five built-in questions. Choose 5 questions for the offline demo."
        )
    return DEMO_QUIZ


def show_source_status() -> None:
    if st.session_state.study_text:
        word_count = len(st.session_state.study_text.split())
        st.success(f"Study material ready: {word_count} words.")
    else:
        st.info("Add study material in the Notes tab before generating a summary or quiz.")


def render_notes_tab(demo_mode: bool) -> None:
    st.subheader("1. Add study material")
    st.write("Upload a text-based PDF or paste notes. Scanned PDFs do not contain selectable text.")

    if demo_mode:
        st.warning(
            "Demo Mode is on. It uses built-in operating-systems notes and fixed sample "
            "results; no Gemini request is made."
        )
        if st.button("Load Demo Notes", type="primary"):
            st.session_state.notes_editor = read_demo_notes()
            save_study_text(st.session_state.notes_editor)
            st.rerun()

    uploaded_file = st.file_uploader("Upload a PDF (maximum 10 MB)", type=["pdf"])
    if uploaded_file and st.button("Extract Text from PDF"):
        try:
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.session_state.notes_editor = extracted_text
            save_study_text(extracted_text)
            st.success("Text was extracted from the PDF. You can review it below.")
        except StudyTextError as error:
            st.error(str(error))

    st.text_area(
        "Or paste your study notes",
        key="notes_editor",
        height=280,
        max_chars=30_000,
        placeholder="Paste a chapter, lecture notes, or an explanation here...",
    )
    if st.button("Use These Notes"):
        try:
            save_study_text(st.session_state.notes_editor)
            st.success("Your study material is ready.")
        except StudyTextError as error:
            st.error(str(error))
    show_source_status()


def render_summary_tab(demo_mode: bool) -> None:
    st.subheader("2. Generate a clear summary")
    show_source_status()
    summary_length = st.radio("Summary length", ["Short", "Medium", "Detailed"], horizontal=True)
    if st.button("Generate Summary", type="primary", disabled=not st.session_state.study_text):
        try:
            with st.spinner("Preparing your summary..."):
                st.session_state.summary = (
                    DEMO_SUMMARY if demo_mode else generate_summary(st.session_state.study_text, summary_length)
                )
            st.success("Summary generated.")
        except AIServiceError as error:
            st.error(str(error))

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        st.download_button(
            "Download Summary (.md)",
            data=st.session_state.summary,
            file_name="ai_studymate_summary.md",
            mime="text/markdown",
        )


def render_quiz_tab(demo_mode: bool) -> None:
    st.subheader("3. Test your understanding")
    show_source_status()
    question_count = st.selectbox("Number of questions", [5, 10, 15])
    if st.button("Generate Quiz", type="primary", disabled=not st.session_state.study_text):
        try:
            with st.spinner("Creating questions from your study material..."):
                if demo_mode:
                    st.session_state.quiz = demo_quiz_for_count(question_count)
                else:
                    raw_quiz = generate_quiz(st.session_state.study_text, question_count)
                    st.session_state.quiz = parse_quiz_response(raw_quiz, question_count)
                reset_quiz()
            st.success("Quiz generated. Select an answer for every question, then submit.")
        except (AIServiceError, QuizValidationError, StudyTextError) as error:
            st.error(str(error))

    questions = st.session_state.quiz
    if not questions:
        return

    answered_count = 0
    answers: dict[int, str] = {}
    for index, question in enumerate(questions):
        st.markdown(f"### Question {index + 1}")
        st.write(question["question"])
        option_labels = [f"{letter}. {text}" for letter, text in question["options"].items()]
        widget_key = f"answer_{st.session_state.quiz_version}_{index}"
        selected_label = st.radio(
            "Choose one answer",
            option_labels,
            index=None,
            key=widget_key,
            label_visibility="collapsed",
            disabled=st.session_state.quiz_submitted,
        )
        if selected_label:
            answers[index] = selected_label[0]
            answered_count += 1

    st.progress(answered_count / len(questions), text=f"Answered {answered_count} of {len(questions)} questions")
    if not st.session_state.quiz_submitted and st.button("Submit Quiz", type="primary"):
        if answered_count != len(questions):
            st.warning("Please answer every question before submitting the quiz.")
        else:
            score, feedback = calculate_score(questions, answers)
            st.session_state.quiz_score = score
            st.session_state.quiz_feedback = feedback
            st.session_state.quiz_submitted = True
            st.rerun()

    if st.session_state.quiz_submitted:
        score = st.session_state.quiz_score
        st.success(f"Your score: {score} / {len(questions)}")
        for index, result in enumerate(st.session_state.quiz_feedback):
            status = "Correct" if result["is_correct"] else "Incorrect"
            with st.expander(f"Question {index + 1}: {status}"):
                st.write(f"Correct answer: **{result['correct_answer']}**")
                st.write(f"Explanation: {result['explanation']}")


def main() -> None:
    initialise_state()
    st.markdown(
        """<style>
        .block-container {max-width: 1050px; padding-top: 2rem;}
        [data-testid="stSidebar"] {background: #f3f7ff;}
        </style>""",
        unsafe_allow_html=True,
    )
    with st.sidebar:
        st.header("AI StudyMate")
        st.caption("Academic project • IBM SkillsBuild Gen AI & Cloud Computing Internship")
        demo_mode = st.toggle("Demo Mode (offline)", value=False)
        st.divider()
        st.subheader("Gemini status")
        if demo_mode:
            st.info("Offline sample content is active.")
        elif get_api_key():
            st.success("API key detected securely.")
        else:
            st.warning("No API key found. Add one or use Demo Mode.")
        st.caption("Your API key is never shown in this app.")

    st.title("📚 AI StudyMate")
    st.write("Turn study material into simple notes and self-checking MCQ quizzes.")
    notes_tab, summary_tab, quiz_tab = st.tabs(["Notes", "Summary", "Quiz"])
    with notes_tab:
        render_notes_tab(demo_mode)
    with summary_tab:
        render_summary_tab(demo_mode)
    with quiz_tab:
        render_quiz_tab(demo_mode)
    st.divider()
    st.caption("AI StudyMate is an academic project. Always verify AI-generated content with your course material.")


if __name__ == "__main__":
    main()
