import io
import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import create_app

@pytest.fixture
def app():
    from app import create_app
    return create_app()

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()

def test_no_audio_upload(client):
    response = client.post('/process-audio')
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_process_audio_invalid_file(client):
    data = {'audio': (io.BytesIO(b"fake data"), 'test.txt')}
    response = client.post('/process-audio', content_type='multipart/form-data', data=data)
    assert response.status_code in [400, 500]