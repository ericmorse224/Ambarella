@echo off
REM ==========================================
REM   AI Meeting Summarizer Setup Script
REM   For Windows Only
REM   Updates for Nextcloud, utils, structure
REM ==========================================

echo.
echo AI Meeting Summarizer - Automated Setup
echo ---------------------------------------
echo.

REM --- Create Python venv if not present ---
if not exist backend\venv (
    echo Creating Python virtual environment...
    python -m venv backend\venv
)

REM --- Activate venv ---
echo Activating virtual environment...
call backend\venv\Scripts\activate

REM --- Upgrade pip and install backend requirements ---
echo.
echo Installing backend dependencies...
pip install --upgrade pip
pip install -r backend\requirements.txt

REM --- Download NLTK data (for Windows, avoid Python prompt) ---
echo.
echo Downloading NLTK punkt tokenizer data...
python -m nltk.downloader punkt

REM --- Frontend setup ---
echo.
echo Installing frontend dependencies...
cd frontend
if not exist node_modules (
    npm install
)
cd ..

echo.
echo Setup complete!
echo ---------------------------------------
echo To run the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python run.py
echo.
echo To run the frontend:
echo    cd frontend
echo    npm run dev
echo.

REM --- Nextcloud warning/help ---
echo If using Nextcloud integration, ensure your credentials are in:
echo    %USERPROFILE%\.app_secrets\env.json
echo Format:
echo    {
echo      "NEXTCLOUD_URL": "https://yourdomain/remote.php/dav",
echo      "NEXTCLOUD_USERNAME": "your_username",
echo      "NEXTCLOUD_PASSWORD": "your_password_or_app_password"
echo    }
echo.

pause
