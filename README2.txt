# AI Meeting Summarizer

An end-to-end system that ingests audio recordings of meetings, transcribes the content, extracts summaries, action items, and decisions, and optionally creates calendar events based on the actions.

## Features

- 🎙️ Audio file upload and validation
- 🔊 Audio pre-processing with FFmpeg (16kHz mono WAV conversion, silence trimming)
- 🧠 Transcription via AssemblyAI
- ✍️ NLP-based summarization and entity/action/decision extraction
- 📅 Zoho Calendar integration for creating events from action items
- 🌐 Web-based dashboard built in React
- 🔒 OAuth 2.0 integration for secure Zoho access

## Folder Structure

```
backend/
├── app.py                  # Main Flask app entry point
├── routes/
│   ├── audio.py            # Audio upload and processing
│   ├── analyze.py          # Transcript NLP analysis
│   └── calendar.py         # Calendar event handling
├── utils/
│   ├── audio_processing.py # FFmpeg helpers
│   ├── summarizer.py       # NLP extraction logic
│   ├── logger.py           # Transcript logging
│   └── zoho_auth.py        # Zoho OAuth blueprint
├── zoho_integration/
│   └── calendar.py         # Calendar API request logic
├── tests/                  # Unit tests for backend
└── .env                    # Environment variables

frontend/
├── src/
│   └── App.jsx             # Main React component
└── public/
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js (for frontend)
- FFmpeg installed and available on PATH

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
ASSEMBLYAI_API_KEY=your_assemblyai_key
ZOHO_CLIENT_ID=your_zoho_client_id
ZOHO_CLIENT_SECRET=your_zoho_secret
ZOHO_REDIRECT_URI=http://localhost:5000/zoho/callback
```

Run the backend:
```bash
flask run
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Running Tests
```bash
cd backend
test
pytest
```

## Status
- ✅ Audio processing and transcription complete
- ✅ NLP summarization and extraction live
- ✅ Zoho calendar integration with event creation
- ✅ Modular Flask codebase
- ✅ React frontend with file upload and results display
- ✅ Unit tests for major components

## License
MIT License

