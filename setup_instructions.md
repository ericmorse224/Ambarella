
# 🛠️ Project Setup Instructions: AI Meeting Summarizer

This document provides step-by-step instructions to install and run the AI Meeting Summarizer project on **Windows**.

---

## 📁 Project Structure

```
ai-meeting-summarizer/
├── backend/
│   ├── run.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── audio_routes.py
│   │   │   ├── json_routes.py
│   │   │   └── zoho_routes.py
│   │   ├── services/
│   │   │   ├── audio_processor.py
│   │   │   ├── calendar_api.py
│   │   │   ├── calendar_integration.py
│   │   │   ├── llm_utils.py
│   │   │   └── nlp_analysis.py
│   │   └── utils/
│   │       ├── entity_utils.py
│   │       ├── logger.py
│   │       ├── logging_utils.py
│   │       ├── nextcloud_utils.py
│   │       └── zoho_utils.py
│   ├── transcripts/
│   ├── logs/
│   ├── uploads/
│   └── tests/
├── frontend/
├── setup.bat
├── README.md
└── setup_instructions.md
```

---

## ✅ Prerequisites

Before getting started, make sure you have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js + npm](https://nodejs.org/)
- [Git](https://git-scm.com/download/win)

---

## ⚙️ 1. Run Setup Script

From the root of the project folder, double-click or run:

```bat
setup.bat
```

This will:

- Create a Python virtual environment and activate it
- Install backend dependencies
- Download NLTK tokenizer data
- Install frontend packages via npm

---

## 🔑 2. Configure Nextcloud Integration

To use Nextcloud calendar features, create a file with your credentials:

**Location:**  
`C:\Users\YOUR_USERNAME\.app_secrets\env.json`  
or  
`~/.app_secrets/env.json` on Linux/macOS

**Format:**
```json
{
  "NEXTCLOUD_URL": "https://yourdomain/remote.php/dav",
  "NEXTCLOUD_USERNAME": "your_username",
  "NEXTCLOUD_PASSWORD": "your_password_or_app_password"
}
```

- Use an [app password](https://docs.nextcloud.com/server/latest/user_manual/en/security/app_passwords.html) if you have 2FA enabled.

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
    { "speaker": "Alice", "text": "We decided to launch next week." },
    { "speaker": "Bob", "text": "I will prepare the documentation." }
  ]
}
```

Response will include:

- Summary
- Extracted action items
- Decisions

---

## 🛠️ Troubleshooting

- If Nextcloud calendar integration fails:
  - Double-check your CalDAV URL, username, and password/app-password in `env.json`
  - Make sure your calendar exists and is accessible
  - Check backend logs: `backend/logs/server.log`

- If Python or npm commands fail:
  - Ensure you are in the correct folder (`backend` or `frontend`)
  - Ensure your virtual environment is activated for backend commands

---

## ❓ Need Help?

- See the [README.md](./README.md) for API usage and advanced configuration.
- For issues, double-check:
    - Python and npm versions
    - That you're in the correct folder before running commands
    - Flask is running in one terminal, React in another

Feel free to reach out to the maintainer or consult the README for updates.

---

Happy coding! 🎉
