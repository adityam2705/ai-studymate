# AI StudyMate

AI StudyMate is a small Streamlit web application that turns study notes into a structured summary and MCQ quiz. It is designed for an academic demonstration and can work offline using its clearly labelled built-in Demo Mode.

## Features

- Upload a text-based PDF or paste notes (up to 30,000 characters).
- Generate short, medium, or detailed Markdown summaries with Gemini.
- Generate 5, 10, or 15 validated MCQs with four options, one answer, and an explanation.
- Submit answers and see the score and explanations only after submission.
- Download a generated summary as a Markdown file.
- Use offline Demo Mode with sample operating-systems notes, a sample summary, and five fixed sample questions.

## Project structure

```text
ai buddy/
├── app.py                 # Streamlit interface and application flow
├── requirements.txt       # Python packages
├── .env.example           # Safe key placeholder only
├── utils/
│   ├── pdf_reader.py      # PDF extraction and note validation
│   ├── ai_service.py      # Gemini API calls and friendly errors
│   ├── quiz_utils.py      # Quiz JSON validation and scoring
│   └── demo_data.py       # Offline sample summary and quiz
├── sample_data/sample_notes.txt
├── tests/                 # Small pytest test suite
├── PROJECT_REPORT.md
└── PPT_CONTENT.md
```

## Run locally on Windows

1. Open this folder in VS Code. Open **Terminal → New Terminal**.
2. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this once in that terminal and retry:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. Install packages:

   ```powershell
   py -m pip install --upgrade pip
   py -m pip install -r requirements.txt
   ```

4. Start the application:

   ```powershell
   py -m streamlit run app.py
   ```

   Streamlit opens a local address (normally `http://localhost:8501`) in a browser. Stop it with `Ctrl+C`.

5. For a fully offline demo, turn on **Demo Mode**, click **Load Demo Notes**, then generate a summary and a 5-question quiz. No internet or API key is required for this mode.

## Configure Gemini securely

1. Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Choose **one** local option—do not put a real key in source code or commit it.

   **Option A — PowerShell environment variable (recommended for this project):**

   ```powershell
   $env:GEMINI_API_KEY="paste_your_key_here"
   py -m streamlit run app.py
   ```

   The variable lasts only for the current terminal session. Close and reopen the terminal, then set it again.

   **Option B — Streamlit secrets:** Create `.streamlit/secrets.toml` locally (it is ignored by Git):

   ```toml
   GEMINI_API_KEY = "paste_your_key_here"
   ```

3. Start the app. The sidebar will say **API key detected securely**. It never displays the key.

The project defaults to `gemini-2.5-flash`. If your key has a different supported model, set `GEMINI_MODEL` before starting the app.

## Run tests

With the virtual environment active, run:

```powershell
py -m pytest -q
```

The tests cover PDF extraction/empty PDF handling, input validation, valid and malformed quiz JSON, and score calculation. They do not make live Gemini calls or test a real API key.

## Deploy to Streamlit Community Cloud

1. Create a new GitHub repository and upload this project. Do **not** upload `.env` or `.streamlit/secrets.toml`.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/), select **Create app**, and choose the repository, branch, and `app.py`.
3. In the app’s settings, open **Secrets** and add:

   ```toml
   GEMINI_API_KEY = "paste_your_key_here"
   ```

4. Save the secret and deploy. The app reads this secret without placing it in the repository.
5. Open the public app and test PDF upload, pasted notes, a summary, quiz generation, and submission.

## Manual checks before submission

- Test a selectable-text PDF and a scanned/empty PDF.
- Test pasted notes shorter than 50 characters and longer than the allowed limit.
- Test a real summary and 5-question quiz with a valid key.
- Test an invalid key (then remove it) to see the friendly error.
- Test Demo Mode offline, including download and quiz submission.

## Gemini SDK note

This project uses Google’s current `google-genai` Python SDK rather than the older `google-generativeai` package. See Google’s [Python quickstart](https://ai.google.dev/gemini-api/docs/get-started) and [API-key guidance](https://ai.google.dev/gemini-api/docs/api-key).
