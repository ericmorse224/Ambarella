
# 📋 AI Meeting Summarizer + Action Tracker + Decision Log

This is a full-stack AI-powered meeting summarization tool:

- **Transcribes meeting audio**
- **Extracts summaries, action items, and decisions**
- **Creates calendar events (Nextcloud CalDAV)**
- **Displays results on a clean React dashboard**

---

## 🚀 Features

- 🎙️ **Audio Transcription** (OpenAI Whisper)
- 🧠 **NLP Summarization** (NLTK, Sumy)
- ✅ **Action Item & Decision Extraction**
- 📅 **Nextcloud Calendar Integration** (self-hosted, private)
- 🌐 **React Dashboard** (Vite, Tailwind CSS)
- 📤 **REST API** (JSON and audio)
- 🔒 **No Google/Microsoft lock-in!**

---

## 🛠️ Tech Stack

### Backend

- Python 3.9+
- Flask (REST API)
- NLTK
- Sumy
- Whisper (OpenAI)
- caldav (for Nextcloud calendar)

### Frontend

- React + Vite
- Tailwind CSS

---

## 📁 Backend Directory Structure

```
backend/
├── run.py
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── audio_routes.py
│   │   ├── json_routes.py
│   │   └── zoho_routes.py
│   ├── services/
│   │   ├── audio_processor.py
│   │   ├── calendar_api.py
│   │   ├── calendar_integration.py
│   │   ├── llm_utils.py
│   │   └── nlp_analysis.py
│   └── utils/
│       ├── entity_utils.py
│       ├── logger.py
│       ├── logging_utils.py
│       ├── nextcloud_utils.py
│       └── zoho_utils.py
├── transcripts/
├── logs/
├── uploads/
├── tests/
```

- `routes/`: Flask Blueprints for main API endpoints (audio, JSON, Zoho).
- `services/`: Audio/NLP/Calendar business logic.
- `utils/`: Entity extraction, logging, Nextcloud and Zoho integrations.
- `logs/`, `uploads/`, `transcripts/`: App data storage.

> **Note:** `meeting_scheduler.py` has been removed (refactored into other modules).  
> `nextcloud_utils.py` provides all Nextcloud calendar integration utilities.

---

## ⚙️ Quick Setup

**Full steps:** see [setup_instructions.md](./setup_instructions.md).

#### 1. (Windows) Run setup script  
```bash
./setup.bat
```

#### 2. Start backend server  
```bash
cd backend
venv\Scriptsctivate
python run.py
```

#### 3. Start frontend dev server  
```bash
cd frontend
npm install
npm run dev
```

---

## 🐳 Docker Deployment

**Run everything in Docker:**
```bash
docker-compose up --build
```
- Backend: [http://localhost:5000](http://localhost:5000)
- Frontend: [http://localhost:5173](http://localhost:5173)

---

## 🔑 Environment & Secrets

### Backend requires:
- **Nextcloud credentials** (`~/.app_secrets/env.json`)
    ```json
    {
      "NEXTCLOUD_URL": "https://yourdomain/remote.php/dav",
      "NEXTCLOUD_USERNAME": "your_username",
      "NEXTCLOUD_PASSWORD": "your_password_or_app_password"
    }
    ```
- These are used for secure calendar event creation.
- **.env file**: Backend can use a `.env` for other secrets (API keys, etc).

---

## 📅 Nextcloud Calendar Integration

**Self-hosted, privacy-first. No Google or Microsoft required.**

### How It Works

- **Action items from meetings become events in your private Nextcloud calendar.**
- Events are visible in Nextcloud web UI or any CalDAV-compatible calendar app (iOS, Android, Outlook, Thunderbird).

### What You Need

- A running [Nextcloud](https://nextcloud.com/) instance (self-hosted, VPS, or company server).
- The "Calendar" app enabled in Nextcloud.
- Your CalDAV calendar link.

### How to Find Your CalDAV Link

1. Open the Calendar app in Nextcloud.
2. Go to calendar settings/info.
3. Copy the CalDAV link.  
   Example:  
   ```
   https://your-domain/remote.php/dav/calendars/yourusername/personal/
   ```

### Setup: Provide Credentials to the App

- Place your CalDAV link, Nextcloud username, and password/app-password in `~/.app_secrets/env.json` (see above).
- **App password is recommended** if using two-factor authentication.
- Restart backend after updating credentials.

### Troubleshooting

- If you get `No calendars found for this user`:
    - Check the CalDAV URL in `env.json`
    - Make sure your Nextcloud calendar is created and the URL is correct
    - Test login in a desktop CalDAV client (Thunderbird, Outlook, etc)
- For calendar creation errors, check backend logs in `backend/logs/server.log`

### Privacy

- **All data and events stay on your server.**
- Nothing is sent to Google, Microsoft, or third parties.

---

## 📤 API Usage Examples

### Transcribe Audio

```
POST http://localhost:5000/process-audio
Content-Type: multipart/form-data
(audio file as 'audio' field)
```

**Response:**
```json
{
  "transcript": "Meeting discussion ...",
  "entities": []
}
```

---

### NLP Summarization

```
POST http://localhost:5000/process-json
Content-Type: application/json
{
  "transcript": "Full meeting transcript here",
  "meeting_id": "optional-meeting-id"
}
```

**Response:**
```json
{
  "summary": [...],
  "actions": [...],
  "decisions": [...],
  "entities": {...},
  "event_logs": [...],  // all events related to this meeting_id
  "warnings": [...],
  "pipeline_version": "v1.4"
}
```

---

### Feedback Endpoint

```
POST http://localhost:5000/feedback
Content-Type: application/json
{
  "meeting_id": "...",
  "user": "...",
  "score": 5,
  "comments": "Great summary"
}
```
---

### Schedule Actions / Calendar Events

```
POST http://localhost:5000/api/schedule-actions
Content-Type: application/json
{
  "actions": [
    {
      "include": true,
      "datetime": "YYYY-MM-DDTHH:MM",
      "text": "Owner will do something",
      "owner": "Owner Name"
    },
    ...
  ]
}
```

**Creates events in Nextcloud for each included action.**

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

## 📌 Roadmap

- [ ] Audio upload from frontend
- [ ] Speaker diarization
- [ ] User authentication
- [x] **Calendar integration (Nextcloud)**
- [ ] Google/Microsoft Calendar (optional)

---

## 📝 License

MIT License. Contributions welcome!

---

## 🙋‍♂️ Questions or Issues?

- Check backend logs in `backend/logs/server.log` for error details.
- Open an issue or PR on GitHub.
- For Nextcloud questions, see the [Nextcloud documentation](https://docs.nextcloud.com/).

---

**Enjoy private, AI-powered meeting management—on your own terms!**
