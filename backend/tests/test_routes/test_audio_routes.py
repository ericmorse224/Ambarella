import io
import pytest
from app import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()

def test_no_audio_upload(client):
    response = client.post('/process-audio')
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_process_audio_invalid_file(client):
    # Upload a non-audio file
    data = {'audio': (io.BytesIO(b"fake data"), 'test.txt')}
    response = client.post('/process-audio', content_type='multipart/form-data', data=data)
    assert response.status_code in [400, 500]
    assert "error" in response.get_json()

def test_process_audio_too_large(client):
    # Simulate an overly large file (fake, just for error path)
    data = {'audio': (io.BytesIO(b"x" * (26 * 1024 * 1024)), 'large.wav')}
    response = client.post('/process-audio', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert "error" in response.get_json()
    assert "too large" in response.get_json()["error"].lower()

@pytest.mark.skip("Requires a valid audio file and Whisper for full integration test")
def test_process_audio_valid_wav(client):
    # You can add a real .wav or .mp3 file here for full end-to-end test
    with open("tests/test_audio/test_sample.wav", "rb") as audio_file:
        data = {'audio': (audio_file, 'test_sample.wav')}
        response = client.post('/process-audio', content_type='multipart/form-data', data=data)
        assert response.status_code == 200
        data = response.get_json()
        assert "transcript" in data
        assert isinstance(data["transcript"], str)
