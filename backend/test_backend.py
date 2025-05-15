import io
import json
import pytest
from run import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_process_audio_missing_file(client):
    response = client.post('/process-audio')
    assert response.status_code == 400

def test_process_audio_invalid_file(client):
    data = {'audio': (io.BytesIO(b"fake data"), 'test.txt')}
    response = client.post('/process-audio', content_type='multipart/form-data', data=data)
    assert response.status_code in [400, 500]

def test_invalid_json_to_process_json(client):
    response = client.post('/process-json', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == "Transcript is empty or missing."

def test_process_json_missing_key(client):
    response = client.post('/process-json', json={})
    assert response.status_code in [400, 500]

