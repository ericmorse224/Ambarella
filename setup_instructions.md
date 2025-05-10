# 🛠️ Project Setup Instructions: AI Meeting Summarizer

This document provides step-by-step instructions to install and run the AI Meeting Summarizer project on **Windows**.

---

## 📁 Project Structure

```
ai-meeting-summarizer/
├── backend/        # Python Flask API with NLP
├── frontend/       # React web dashboard
├── setup.bat       # Windows setup script (runs everything)
├── README.md       # Project overview
└── setup_instructions.md  # This file
```

---

## ✅ Prerequisites

Before getting started, make sure you have the following installed:

* [Python 3.9+](https://www.python.org/downloads/)
* [Node.js + npm](https://nodejs.org/)
* [Git](https://git-scm.com/download/win)

---

## ⚙️ 1. Run Setup Script

From the root of the project folder, double-click or run:

```bat
setup.bat
```

This will:

* Create a Python virtual environment and activate it
* Install backend dependencies
* Download NLTK tokenizer data
* Install frontend packages via npm

---

## 🧪 2. Sample Data

A test file is provided at:

```
backend/meeting_data/sample_meeting.json
```

Use it to test the `/process-json` endpoint.

---

## 🚀 3. Run Backend

Open a terminal and run:

```bash
cd backend
venv\Scripts\activate
python run.py
```

Backend will run at: `http://127.0.0.1:5000`

---

## 🌐 4. Run Frontend

In a **new terminal**:

```bash
cd frontend
npm run dev
```

Frontend will run at: `http://localhost:5173`

---

## 🔁 5. Test the Workflow

Use a tool like **Postman** or a simple frontend form to send a `POST` request to:

```
POST http://127.0.0.1:5000/process-json
```

With JSON body:

```json
{
  "transcript": [
    { "speaker": "Alice", "text": "We decided to launch next week." ***REMOVED***,
    { "speaker": "Bob", "text": "I will prepare the documentation." ***REMOVED***
  ]
***REMOVED***
```

Response will include:

* Summary
* Extracted action items
* Decisions

---

## ❓ Need Help?

For any issues, double-check:

* Python and npm versions
* That you're in the correct folder before running commands
* Flask is running in one terminal, React in another

Feel free to reach out to the maintainer or consult the README for updates.

---

Happy coding! 🎉
