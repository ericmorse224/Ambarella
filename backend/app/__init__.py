from flask import Flask
from flask_cors import CORS

# Import blueprints
from app.routes.audio_routes import audio_bp
from app.routes.json_routes import json_bp
from app.services.calendar_api import calendar_api

def create_app():
    app = Flask(__name__)
    print(app.url_map)

    # Enable CORS for frontend
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Set file upload limit to 50MB
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

    # Register blueprints
    app.register_blueprint(audio_bp)
    app.register_blueprint(json_bp)
    app.register_blueprint(calendar_api)

    return app
