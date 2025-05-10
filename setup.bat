@echo off
echo Setting up Python virtual environment...

cd backend
python -m venv venv
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo Downloading NLTK data...
python -m nltk.downloader punkt

cd ..
echo Python backend setup complete.

echo Setting up React frontend...
cd frontend
npm install

echo React frontend setup complete.
pause
