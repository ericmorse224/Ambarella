import pytest
from unittest.mock import patch
from datetime import datetime, timedelta

@pytest.fixture
def app():
    from app import create_app
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()

def test_zoho_auth_redirect(client):
    response = client.get("/zoho/auth")
    assert response.status_code == 302  # Should redirect to Zoho login

@patch("app.routes.zoho_routes.get_user_profile")
def test_zoho_user_success(mock_profile, client):
    mock_profile.return_value = {"email": "test@example.com"}
    response = client.get("/zoho/user")
    assert response.status_code == 200
    assert response.get_json()["email"] == "test@example.com"

@patch("app.routes.zoho_routes.create_calendar_event")
def test_create_event_success(mock_create, client):
    mock_create.return_value = {"status": "success"}
    sample_data = {
        "events": [
            {"text": "Send slides", "owner": "Alice", "startTime": "2025-05-15T10:00:00Z"}
        ]
    }
    response = client.post("/create-event", json=sample_data)
    assert response.status_code == 200
    assert response.get_json()["success"] is True

@patch("app.routes.zoho_routes.create_calendar_event", side_effect=Exception("Failure"))
def test_create_event_failure(mock_create, client):
    bad_data = {
        "events": [
            {"text": "Broken event", "owner": "Alice", "startTime": "2025-05-15T10:00:00Z"}
        ]
    }
    response = client.post("/create-event", json=bad_data)
    assert response.status_code == 500
    assert "error" in response.get_json()

@patch("app.routes.zoho_routes.requests.post")
def test_get_zoho_token_success(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"access_token": "mock_token"}
    response = client.get("/api/zoho-token")
    assert response.status_code == 200
    assert "access_token" in response.get_json()

@patch("app.routes.zoho_routes.requests.post")
def test_get_zoho_token_failure(mock_post, client):
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "Token error"
    response = client.get("/api/zoho-token")
    assert response.status_code == 500
    assert "error" in response.get_json()
@patch("app.routes.zoho_routes.requests.post")
def test_zoho_callback_success(mock_post, client):
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {
        "access_token": "new_token",
        "refresh_token": "refresh_token"
    }
    response = client.get("/zoho/callback?code=mock_code")
    assert response.status_code == 200
    assert "access_token" in response.get_json()

@patch("app.routes.zoho_routes.requests.post")
def test_zoho_callback_failure(mock_post, client):
    mock_post.return_value.ok = False
    mock_post.return_value.text = "Failed exchange"
    response = client.get("/zoho/callback?code=invalid_code")
    assert response.status_code == 500
    assert "error" in response.get_json()

def test_blueprints_registered(app):
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert "/zoho/auth" in rules
    assert "/zoho/callback" in rules
    assert "/zoho/user" in rules
    assert "/create-event" in rules
    assert "/api/zoho-token" in rules