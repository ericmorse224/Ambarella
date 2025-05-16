# 📋 AI Meeting Summarizer + Action Tracker + Decision Log

This is a full-stack AI-powered meeting summarization tool that:

* Transcribes audio or parses meeting JSON
* Extracts summaries, action items, and decisions
* Displays results on a clean React dashboard

---

## 🚀 Features

* 🎙️ **Audio Transcription** using Deepgram API
* 🧠 **NLP Summarization** with Sumy + NLTK
* ✅ **Action Item & Decision Extraction**
* 📅 **Calendar Metadata Parsing** from JSON
* 🌐 **React Dashboard** for meeting insights

---

## 🛠️ Tech Stack

### Backend

* Python 3.9+
* Flask
* NLTK
* Sumy
* Deepgram SDK

### Frontend

* React + Vite
* Tailwind CSS (optional styling)

---

## 📁 Project Structure


### 📁 Backend Folder Structure

```plaintext
backend/
├── run.py                             # Entry point: starts Flask app using factory
├── __init__.py                        # (optional) backend package marker

├── app/
│   ├── __init__.py                    # Flask app factory: registers blueprints
│
│   ├── routes/                        # Flask route modules (Blueprints)
│   │   ├── __init__.py
│   │   ├── audio_routes.py            # /process-audio
│   │   ├── json_routes.py             # /process-json, /process-json-for-AB-testing
│   │   └── zoho_routes.py             # /zoho/auth, /callback, /create-event
│
│   ├── services/                      # Business logic & integrations
│   │   ├── __init__.py
│   │   ├── audio_processor.py         # convert_to_wav, trim_silence
│   │   ├── calendar_api.py            # create_calendar_event, get_user_profile
│   │   ├── calendar_integration.py    # extract_event_times, auto_schedule_actions
│   │   ├── llm_utils.py               # clean_transcript, generate_summary_and_extraction, parse_llm_sections
│   │   ├── meeting_scheduler.py       # create/update Zoho Meetings
│   │   └── nlp_analysis.py            # analyze_transcript()
│
│   ├── utils/                         # Stateless shared helpers
│   │   ├── __init__.py
│   │   ├── entity_utils.py            # extract_people, assign_owner, etc.
│   │   ├── logger.py                  # rotating file + console logger instance
│   │   ├── logging_utils.py           # log_transcript_to_file()
│   │   └── zoho_utils.py              # token mgmt, authorized calendar/meeting API wrappers

├── transcripts/                       # Saved transcripts (via logging_utils)
├── logs/                              # Server logs written by logger.py
├── uploads/                           # Temporary uploaded audio

├── tests/                             # (optional) unit/integration test files
│   ├── test_audio.py
│   ├── test_llm_utils.py
│   └── test_routes.py
```


ai-meeting-summarizer/
├── backend/        # Flask app (API + NLP)
├── frontend/       # React app
├── setup.bat       # One-click setup for Windows
├── setup_instructions.md
├── Dockerfile      # Backend Docker image
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Setup Instructions

For full installation steps, see [setup\_instructions.md](./setup_instructions.md).

Quick start:

```bash
# 1. Run setup script (Windows only)
./setup.bat

# 2. Start backend
cd backend
venv\Scripts\activate
python run.py

# 3. Start frontend
cd frontend
npm run dev
```

---

## 🐳 Docker Deployment

Build and run both frontend and backend services with Docker Compose:

### 1. Create `Dockerfile` in `backend/`:

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### 2. Create `docker-compose.yml` in root:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"

  frontend:
    working_dir: /app
    image: node:18-alpine
    volumes:
      - ./frontend:/app
    ports:
      - "5173:5173"
    command: sh -c "npm install && npm run dev"
```

### 3. Run containers:

```bash
docker-compose up --build
```

Visit:

* Backend: [http://localhost:5000](http://localhost:5000)
* Frontend: [http://localhost:5173](http://localhost:5173)

---

## 📤 Example Input

Send a POST request to:

```
POST http://localhost:5000/process-json
```

With body:

```json
{
  "transcript": [
    { "speaker": "Alice", "text": "We decided to ship the product next week." },
    { "speaker": "Bob", "text": "I'll write the release notes and handle deployment." }
  ]
}
```

---

## 📈 Output Example

```json
{
  "summary": ["We decided to ship the product next week."],
  "actions": ["I'll write the release notes and handle deployment."],
  "decisions": ["We decided to ship the product next week."]
}
```

---

## 📌 To-Do / Roadmap

* [ ] Upload audio from frontend
* [ ] Speaker diarization (from transcript)
* [ ] User authentication
* [ ] Calendar integration (Google/Microsoft API)

---

## 📝 License

MIT License. Contributions welcome!