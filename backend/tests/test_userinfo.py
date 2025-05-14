import sys
import os
import json
from flask import Flask, jsonify
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock user info to simulate Zoho API response
mock_userinfo_response = {
    "Email": "user@example.com",
    "Display_Name": "Zoho User"
***REMOVED***

# Simulated Flask app with /zoho/userinfo route
def create_test_app():
    app = Flask(__name__)

    @app.route('/zoho/userinfo')
    def userinfo():
        return jsonify(mock_userinfo_response)

    return app

# Unit test for user info endpoint
def test_zoho_userinfo_endpoint():
    app = create_test_app()
    client = app.test_client()

    response = client.get('/zoho/userinfo')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["Email"] == "user@example.com"
    assert data["Display_Name"] == "Zoho User"
