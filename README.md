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

