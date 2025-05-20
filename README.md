
# 📋 AI Meeting Summarizer + Action Tracker + Decision Log

[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![React](https://img.shields.io/badge/React-19-blue)](https://react.dev/)
[![Nextcloud](https://img.shields.io/badge/Nextcloud-Calendar-blue)](https://nextcloud.com/)

## Why use this tool?

**Automate your meeting notes and actions—privately!**  
No more scrambling to remember who promised what. This full-stack, AI-powered solution securely transcribes meeting audio, generates smart summaries, extracts action items and decisions, and allows you to schedule follow-ups in your **own** Nextcloud calendar.  
_Your data stays on your infrastructure—never sent to Google or Microsoft._

---

## 🌟 Features

- 🎙️ **Audio Transcription:** Uses Whisper for accurate, fast meeting transcription.
- 🧠 **Automatic Summarization:** Get concise meeting summaries with NLTK & Sumy.
- ✅ **Action Item & Decision Extraction:** AI highlights “who will do what, by when.”
- 📅 **Nextcloud Calendar Integration:** Seamlessly turns action items into private calendar events.
- 🌐 **Modern React Dashboard:** Fast, responsive UI with Vite & Tailwind CSS.
- 📤 **RESTful API:** For audio and JSON transcript processing.
- 🧪 **Full Testing Coverage:** Vitest + Playwright.
- 🔒 **Zero Vendor Lock-in:** No Google, no Microsoft, no cloud lock.

---

## 🚀 Quick Start

> **Full details:** See [`setup_instructions.md`](./setup_instructions.md).

### 1. Clone the repository

```bash
git clone https://github.com/emorse224/meeting-summary-dashboard.git
```

### 2. Backend setup (Python 3.9+)

```bash
cd backend
python -m venv venv
venv\Scriptsctivate         # On Windows
source venv/bin/activate     # On Mac/Linux
pip install -r requirements.txt
python run.py
```

### 3. Frontend setup (React 19)

```bash
cd frontend
npm install
npm start
```
- Frontend runs at [http://localhost:3000](http://localhost:3000)
- Backend runs at [http://localhost:5000](http://localhost:5000)

### 4. Docker (optional, all-in-one)

```bash
docker-compose up --build
```
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://localhost:5000](http://localhost:5000)

---

## 🔑 Environment & Secrets

- **Backend:** Place your Nextcloud credentials in `~/.app_secrets/env.json`:

    ```json
    {
      "NEXTCLOUD_URL": "https://yourdomain/remote.php/dav",
      "NEXTCLOUD_USERNAME": "your_username",
      "NEXTCLOUD_PASSWORD": "your_password_or_app_password"
    }
    ```
- Use app passwords if you have Nextcloud 2FA.
- `.env` file for Whisper, Nexcloud, etc.

---

## 📅 Nextcloud Calendar Integration

**Your actions, your calendar, your privacy.**

- Action items auto-create private calendar events.
- Works with any CalDAV-compatible client (iOS, Android, Outlook, Thunderbird).
- Setup: Find your CalDAV link (Nextcloud Calendar > Settings > Info), add to `env.json`, restart backend.

---

## 📤 API Usage Examples

### Transcribe Audio

```http
POST /process-audio
Content-Type: multipart/form-data
(audio file as 'audio' field)
```
**Response:**
```json
{ "transcript": "...", "entities": [] }
```

### Summarize Transcript

```http
POST /process-json
Content-Type: application/json
{ "transcript": "...", "entities": [] }
```
**Response:**
```json
{ "summary": [...], "actions": [...], "decisions": [...] }
```

### Schedule Actions

```http
POST /api/schedule-actions
Content-Type: application/json
{
  "actions": [
    {
      "include": true,
      "datetime": "YYYY-MM-DDTHH:MM",
      "text": "Owner will do something",
      "owner": "Owner Name"
    }
  ]
}
```

---

## 🗂️ Project Structure

<details>
<summary>Click to expand</summary>

### Frontend

```
frontend/
  public/
  src/
    App.jsx
    components/
      AudioUploadForm.jsx
      CalendarEventForm.jsx
      DecisionsPanel.jsx
      ErrorBoundary.jsx
      NextcloudConnect.jsx
      ReviewPanel.jsx
      SummaryPanel.jsx
      TranscriptPanel.jsx
    hooks/
      UseMeetingState.jsx
    utils/
      dateUtils.js
    tests/
      unit/
      integration/
      e2e/
    index.js
    index.css
    setupTests.js
  tailwind.config.js
  postcss.config.js
  vite.config.js
  package.json
```

### Backend

```
backend/
  run.py
  app/
    __init__.py
    routes/
      audio_routes.py
      json_routes.py
    services/
      audio_processor.py
      calendar_integration.py
      llm_utils.py
      nlp_analysis.py
    utils/
      entity_utils.py
      logger.py
      logging_utils.py
      nextcloud_utils.py
  transcripts/
  logs/
  uploads/
  tests/
```

</details>

---

## 🧪 Testing & Coverage

- **Vitest** for frontend/unit/integration
- **Playwright** for end-to-end
- Coverage >95%
- Run all tests:
  ```bash
  npm test
  ```

---

## 📌 Roadmap

- [ ] Speaker diarization (who spoke when)
- [ ] User authentication
- [ ] Google/Microsoft Calendar support (optional)

---

## 📝 License

This project is licensed under [GNU GPLv3](LICENSE).

---

## 🙋‍♂️ Support & Questions

- Check backend logs at `backend/logs/server.log`
- [Open an issue](https://github.com/emorse224/meeting-summary-dashboard/issues) or submit a PR
- Nextcloud help: [Nextcloud Docs](https://docs.nextcloud.com/)

---

**Enjoy secure, private, AI-powered meeting management!**
