from unittest.mock import Mock
import pytest
from unittest.mock import patch
from app.utils.zoho_utils import create_meeting, get_user_profile

@patch("app.utils.zoho_utils.make_authorized_request")
def test_create_meeting_success(mock_request):
    mock_request.return_value.ok = True
    mock_request.return_value.json.return_value = {"meeting_url": "https://mock.zoho.meeting"}
    
    response = create_meeting("Weekly Sync", "Team updates", "2025-05-14T15:00:00Z")
    assert response["meeting_url"] == "https://mock.zoho.meeting"

@patch("app.utils.zoho_utils.make_authorized_request")
def test_create_meeting_failure(mock_request):
    mock_request.return_value.ok = False
    mock_request.return_value.text = "Unauthorized"
    
    response = create_meeting("Fail Test", "No access", "2025-05-14T15:00:00Z")
    assert response is None

@patch("app.utils.zoho_utils.requests.get")
@patch("app.utils.zoho_utils.load_access_token", return_value="fake_token")
def test_get_user_profile_success(mock_token, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {"email": "test@example.com"}
    
    response = get_user_profile()
    assert response["email"] == "test@example.com"

@patch("app.utils.zoho_utils.requests.get")
@patch("app.utils.zoho_utils.load_access_token", return_value="expired_token")
@patch("app.utils.zoho_utils.refresh_access_token", return_value="new_token")
def test_get_user_profile_refresh(mock_refresh, mock_token, mock_get):
    # Simulate first call 401, second call success
    mock_get.side_effect = [
        Mock(status_code=401),
        Mock(status_code=200, ok=True, json=lambda: {"email": "refreshed@example.com"})
    ]
    
    response = get_user_profile()
    assert response["email"] == "refreshed@example.com"