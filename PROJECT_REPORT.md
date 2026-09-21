# AI StudyMate – AI-Powered Study Notes Summarizer and Quiz Generator

## 1. Project title

**AI StudyMate – AI-Powered Study Notes Summarizer and Quiz Generator**

## 2. Abstract

AI StudyMate is a simple web application that helps students work with lengthy study material. A student can upload a text-based PDF or paste notes, generate an easy-to-read summary, and create a multiple-choice quiz based on the same material. The application uses Python and Streamlit for the interface, PyPDF for PDF text extraction, and the Google Gemini API for generative-AI features. It also contains an offline Demo Mode with fixed sample notes, summary, and questions so the project can be demonstrated without an internet connection or API key.

## 3. Introduction

Students often receive long chapters, lecture notes, and reference material. Reading and revising all content can take considerable time. Generative AI can support revision by converting provided material into concise notes and practice questions. AI StudyMate is intentionally small and easy to understand: it does not replace learning or a teacher; it helps students review their own material.

## 4. Problem statement

Students need a convenient way to identify the main ideas in long study notes and test their understanding. Manual summarization and question creation take time. Existing generic AI tools may not clearly limit questions to the supplied notes, may require complicated setup, or may not provide an offline demonstration option.

## 5. Objectives

- Accept study material as a text-based PDF or pasted text.
- Validate that the material is readable and within a reasonable size limit.
- Generate structured, student-friendly summaries using Gemini.
- Generate MCQs based only on the provided material.
- Show score, correct answers, and explanations after quiz submission.
- Provide downloadable summaries and a transparent offline Demo Mode.
- Prepare the application for local use and Streamlit Community Cloud deployment.

## 6. Existing system and proposed system

| Existing approach | Proposed AI StudyMate approach |
| --- | --- |
| Students manually read and shorten notes. | Gemini creates a structured summary from supplied material. |
| Practice questions are written manually or found elsewhere. | Gemini produces MCQs tied to the current notes, then the app validates their structure. |
| Many AI demonstrations require a live connection. | Clearly labelled Demo Mode uses fixed local sample data. |
| Answers may appear alongside questions. | Correct answers are shown only after the student submits the quiz. |

## 7. Hardware and software requirements

### Hardware

- A laptop or desktop computer capable of running Python 3.9 or later.
- Internet access only when using live Gemini generation or deploying to the cloud.

### Software

- Windows 10/11 (tested instructions are for Windows; other operating systems can use equivalent commands).
- Python 3.9 or later.
- VS Code or another code editor (optional but recommended).
- Python packages: Streamlit, google-genai, PyPDF, and pytest.
- A Gemini API key for live AI features.

## 8. Technology stack

- **Python:** Application logic and utility functions.
- **Streamlit:** Web interface, widgets, session state, downloads, and sidebar.
- **Google Gemini API (`google-genai` SDK):** Live summary and quiz generation.
- **PyPDF:** Extraction of selectable text from PDF documents.
- **pytest:** Small automated test suite.
- **Streamlit Community Cloud:** Optional cloud deployment platform.

## 9. System architecture

```text
Student
   │ uploads PDF / pastes notes
   ▼
Streamlit interface (app.py)
   │
   ├── pdf_reader.py → validate and extract selectable text
   ├── Demo Mode → local sample notes, summary, and quiz (no API call)
   └── ai_service.py → Gemini API → summary or quiz JSON
                                      │
                                      ▼
                         quiz_utils.py validates JSON and scores answers
                                      │
                                      ▼
                            Streamlit displays/downloads results
```

## 10. Module descriptions

- **`app.py`:** Main Streamlit application. It presents tabs, buttons, status messages, session state, quiz UI, progress, and download functionality.
- **`utils/pdf_reader.py`:** Checks text length, file size, and PDF readability. It explains when a PDF is empty, scanned, corrupted, or otherwise unreadable.
- **`utils/ai_service.py`:** Reads the API key safely, sends prompts to Gemini, and turns technical API problems into beginner-friendly messages.
- **`utils/quiz_utils.py`:** Parses Gemini’s expected JSON quiz format, rejects malformed data, and calculates quiz scores.
- **`utils/demo_data.py`:** Stores the transparent fixed data used only when Demo Mode is selected.
- **`sample_data/sample_notes.txt`:** Local operating-systems notes for an offline demonstration.
- **`tests/`:** Automated checks for extraction, validation, quiz parsing, and scoring.

## 11. Implementation details

The user first adds notes in the Notes tab. The application requires at least 50 characters and limits material to 30,000 characters. For a PDF, PyPDF extracts text page by page. If no text is found, the user is advised that the document may be scanned and can paste the text instead.

For a live summary, the application sends the selected note length and supplied material to Gemini. The prompt asks for headings, bullet points, definitions, and facts supported by the notes. A Markdown download button saves the generated result.

For a live quiz, the prompt asks Gemini for JSON with a strict structure: question, options A–D, one correct-answer letter, and explanation. The program validates every question before showing it. Answers are kept in Streamlit session state, and explanations are withheld until the user submits all answers.

The API key is read from `GEMINI_API_KEY` / `GOOGLE_API_KEY` environment variables or Streamlit secrets. It is not stored in source code, printed, or displayed. Demo Mode deliberately avoids the Gemini service and marks its sample output as offline data.

## 12. Testing and results

Automated tests included with the project check:

- Extraction of selectable text from a small valid PDF.
- Rejection of an empty or malformed PDF.
- Rejection of too-short notes.
- Acceptance of a valid quiz JSON response.
- Rejection of malformed JSON and missing quiz options.
- Score calculation and feedback for an incorrect answer.

Run `py -m pytest -q` to record the actual test result on the demonstration laptop. The project does not claim a live Gemini result until it has been tested with the student’s own valid API key and notes.

**Fill in after your run:**

- Date tested: ____________________
- Python version: ____________________
- pytest result: ____________________
- Live Gemini model used: ____________________
- One example subject/PDF tested: ____________________

## 13. Limitations

- Scanned image-only PDFs cannot be read because OCR is not included.
- Live generation requires internet access, a valid Gemini API key, and available quota.
- AI output can be incomplete or inaccurate, so students must compare it with course material.
- The simple local version does not save user accounts, documents, or quiz history.
- Demo Mode contains five fixed questions only; it is intended for offline presentation, not personalized generation.

## 14. Future scope

- Add OCR for scanned PDFs.
- Support DOCX and image uploads.
- Allow students to choose difficulty level and topic focus.
- Add flashcards, quiz-history storage, and subject folders.
- Add teacher review, editable questions, and export to PDF.
- Introduce multilingual summaries and accessibility options.

## 15. Conclusion

AI StudyMate demonstrates a focused application of generative AI in education. It combines simple Python modules with Streamlit, PyPDF, and Gemini to make supplied study material easier to revise and practice. The application maintains a beginner-friendly architecture, validates important inputs and AI quiz responses, handles common errors, protects API keys, and provides an honest offline demonstration path.
