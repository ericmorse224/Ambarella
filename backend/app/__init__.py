from flask import Flask
from flask_cors import CORS

# Import blueprints
from app.routes.zoho_routes import zoho_bp
from app.routes.audio_routes import audio_bp
from app.routes.json_routes import json_bp

def create_app():
    app = Flask(__name__)

    # Enable CORS for frontend
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Set file upload limit to 25MB
    app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

    # Register blueprints
    app.register_blueprint(zoho_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(json_bp)

    return app
