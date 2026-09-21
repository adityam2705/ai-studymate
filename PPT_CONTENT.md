# AI StudyMate – 8-Slide Presentation Content

Use this as concise content for a 5–7 minute presentation. Replace all items marked **[Fill in]** only after you run the project.

## Slide 1 — Title and introduction

**AI StudyMate**

AI-Powered Study Notes Summarizer and Quiz Generator

- Academic project for IBM SkillsBuild Gen AI & Cloud Computing Internship
- Presented by: **[Fill in your name, roll number, college]**
- Converts supplied study material into summaries and practice quizzes

Speaker note: Introduce the problem: students have long notes but limited revision time.

## Slide 2 — Problem statement

- Long study notes are time-consuming to review.
- Creating practice questions manually takes extra effort.
- Generic outputs may not be focused on the student’s supplied material.
- A college demonstration should also work when internet access is unavailable.

## Slide 3 — Objectives and scope

- Upload a text-based PDF or paste notes.
- Generate short, medium, or detailed structured summaries.
- Generate MCQs with four options, one answer, and explanations.
- Show answers only after quiz submission.
- Download the summary.
- Provide clearly labelled offline Demo Mode.

## Slide 4 — Technology stack

- Python: application logic
- Streamlit: simple web interface
- Google Gemini API: live generative-AI summary and quiz generation
- PyPDF: selectable-text extraction from PDFs
- pytest: basic automated validation
- Streamlit Community Cloud: optional deployment

## Slide 5 — System architecture and workflow

```text
PDF / pasted notes → validation and text extraction
                         ↓
             Demo Mode OR Gemini API generation
                         ↓
       Summary download / validated quiz / score and feedback
```

- API key stays in environment variables or Streamlit secrets.
- Quiz JSON is validated before it is shown.
- Demo Mode uses fixed sample data and makes no AI request.

## Slide 6 — Implementation and screenshots to capture

- Streamlit app with Notes, Summary, and Quiz tabs.
- Sidebar showing Demo Mode and secure API status.
- PDF validation and friendly error messages.
- Session state preserves generated output during normal interactions.

Add these screenshots after running the app:

1. Notes tab with sample notes loaded.
2. Generated summary and download button.
3. Quiz before submission (no correct answers visible).
4. Quiz score and explanations after submission.
5. Optional: Demo Mode sidebar or unreadable-PDF error.

## Slide 7 — Testing and results

- Automated tests cover PDF extraction, empty PDF handling, input validation, quiz parsing, and scoring.
- Manual tests: live Gemini summary/quiz, invalid key message, Demo Mode, and download.
- Result from local test run: **[Fill in `pytest` output]**
- Live model and sample subject used: **[Fill in after testing]**

Do not add performance claims or screenshots that were not actually captured.

## Slide 8 — Conclusion and future scope

- AI StudyMate is a small, explainable study-support web app.
- It combines note summarization with self-assessment from the same material.
- It handles basic validation, malformed AI output, and API errors.
- Offline Demo Mode supports a reliable academic demonstration.

Future scope: OCR for scanned PDFs, multiple file types, flashcards, difficulty selection, user history, and multilingual support.

Thank you — Questions?
