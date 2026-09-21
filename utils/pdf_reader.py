"""Read and validate text from student-provided notes."""

from __future__ import annotations

from pypdf import PdfReader

MAX_PDF_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB keeps local demos responsive.
MAX_TEXT_CHARACTERS = 30_000
MIN_TEXT_CHARACTERS = 50


class StudyTextError(ValueError):
    """Raised when uploaded or pasted study material cannot be used."""


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract selectable text from a Streamlit UploadedFile or binary file."""
    file_size = getattr(uploaded_file, "size", None)
    if file_size is not None and file_size > MAX_PDF_SIZE_BYTES:
        raise StudyTextError("Please upload a PDF smaller than 10 MB.")

    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        reader = PdfReader(uploaded_file)
        extracted_pages = [page.extract_text() or "" for page in reader.pages]
    except Exception as error:  # pypdf uses different errors for malformed files.
        raise StudyTextError(
            "This PDF could not be read. It may be corrupted, password-protected, "
            "or not a valid PDF."
        ) from error

    text = "\n".join(extracted_pages).strip()
    if not text:
        raise StudyTextError(
            "No readable text was found. This may be a scanned or empty PDF. "
            "Try pasting the notes as text instead."
        )
    return validate_study_text(text)


def validate_study_text(text: str) -> str:
    """Return clean text after applying friendly length checks."""
    if not isinstance(text, str):
        raise StudyTextError("Study material must be text.")

    clean_text = text.strip()
    if len(clean_text) < MIN_TEXT_CHARACTERS:
        raise StudyTextError(
            "Please provide at least 50 characters of meaningful study material."
        )
    if len(clean_text) > MAX_TEXT_CHARACTERS:
        raise StudyTextError(
            "The notes are too long for this simple project. Please use 30,000 "
            "characters or fewer, or summarize one chapter at a time."
        )
    return clean_text
