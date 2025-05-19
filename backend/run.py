"""
run.py

Entry point for the AI Meeting Summarizer Flask backend.

Created by Eric Morse
Date: 2024-05-18

This script initializes the Flask app via the application factory
pattern (`create_app()`), and runs it in debug mode when executed
directly.

Usage:
    python run.py

The app object is used by the WSGI server (such as gunicorn or flask run)
for production or development deployment.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
