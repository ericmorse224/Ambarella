import os
import io
import pytest
from app import create_app
from app.services import audio_processor

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

def test_process_audio_too_large(client, tmp_path):
    # Create a large file
    big_file = tmp_path / "big.wav"
    big_file.write_bytes(b"\0" * 60 * 1024 * 1024)
    with open(big_file, "rb") as f:
        resp = client.post('/audio', data={'audio': (f, "big.wav")}, content_type='multipart/form-data')
    assert resp.status_code in (400, 404, 413)
    # Optionally print the response for future debugging
    print("Status:", resp.status_code, "Body:", resp.data)

def test_process_audio_valid_wav(client):
    # You can add a real .wav or .mp3 file here for full end-to-end test
    with open("tests/test_audio/All_Needs.wav", "rb") as audio_file:
        data = {'audio': (audio_file, 'test_sample.wav')}
        response = client.post('/process-audio', content_type='multipart/form-data', data=data)
        assert response.status_code == 200
        data = response.get_json()
        assert "transcript" in data
        assert isinstance(data["transcript"], str)

def test_upload_audio_missing_file(client):
    resp = client.post('/audio', data={})
    assert resp.status_code in (400, 404, 413, 422)

def test_process_audio_no_file(client):
    resp = client.post('/process-audio', data={})
    assert resp.status_code == 400
    assert "Invalid file" in resp.get_json()["error"]

def test_process_audio_non_audio_file(client, tmp_path):
    bad_file = tmp_path / "not_audio.txt"
    bad_file.write_text("not audio")
    with open(bad_file, "rb") as f:
        resp = client.post('/process-audio', data={'audio': (f, "not_audio.txt")}, content_type='multipart/form-data')
    assert resp.status_code == 400
    assert "Invalid file" in resp.get_json()["error"]

def test_process_audio_empty_file(client, tmp_path):
    empty_file = tmp_path / "empty.wav"
    empty_file.write_bytes(b"")
    with open(empty_file, "rb") as f:
        resp = client.post('/process-audio', data={'audio': (f, "empty.wav")}, content_type='multipart/form-data')
    # It should fail quality check or produce an error
    assert resp.status_code in (400, 500)

def test_process_audio_get_not_allowed(client):
    resp = client.get('/process-audio')
    assert resp.status_code == 405

def test_process_audio_put_not_allowed(client):
    resp = client.put('/process-audio')
    assert resp.status_code == 405

def test_process_audio_delete_not_allowed(client):
    resp = client.delete('/process-audio')
    assert resp.status_code == 405

def test_process_audio_backend_error(client, tmp_path, monkeypatch):
    # Monkeypatch to simulate a failure that is caught in route logic
    monkeypatch.setattr(audio_processor, "check_audio_quality", lambda f: (True, None))
    monkeypatch.setattr(audio_processor, "convert_to_wav", lambda *a, **k: (_ for _ in ()).throw(Exception("conversion failed")))
    test_file = tmp_path / "sample.wav"
    test_file.write_bytes(b"\x00" * 1024)
    with open(test_file, "rb") as f:
        resp = client.post('/process-audio', data={'audio': (f, "sample.wav")}, content_type='multipart/form-data')
    assert resp.status_code == 400
    # Accept any error message (all indicate backend failure)
    data = resp.get_json()
    assert "error" in data

def test_process_audio_file_too_large(client, tmp_path):
    big_file = tmp_path / "huge.wav"
    big_file.write_bytes(b"\0" * (26 * 1024 * 1024))  # 26MB
    with open(big_file, "rb") as f:
        resp = client.post('/process-audio', data={'audio': (f, "huge.wav")}, content_type='multipart/form-data')
    assert resp.status_code in (413, 500)
    # Optionally, print for debugging
    print("Too large status:", resp.status_code, resp.get_data(as_text=True))

def test_process_audio_unhandled_server_error(client, tmp_path, monkeypatch):
    # Patch the last function called to raise an uncaught Exception
    monkeypatch.setattr(audio_processor, "check_audio_quality", lambda f: (True, None))
    monkeypatch.setattr(audio_processor, "convert_to_wav", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("unhandled error")))
    test_file = tmp_path / "audio.wav"
    test_file.write_bytes(b"\x00" * 1024)
    with open(test_file, "rb") as f:
        resp = client.post('/process-audio', data={'audio': (f, "audio.wav")}, content_type='multipart/form-data')
    # Should hit the generic exception handler
    assert resp.status_code == 400 or resp.status_code == 500
    assert "error" in resp.get_json()

def test_process_audio_uncaught_exception(client, tmp_path, monkeypatch):
    # Simulate unhandled error late in the route
    monkeypatch.setattr(audio_processor, "check_audio_quality", lambda f: (True, None))
    def raise_final(*a, **k): raise RuntimeError("unexpected failure")
    monkeypatch.setattr(audio_processor, "convert_to_wav", raise_final)
    test_file = tmp_path / "unhandled.wav"
    test_file.write_bytes(b"\x00" * 1024)
    with open(test_file, "rb") as f:
        resp = client.post('/process-audio', data={'audio': (f, "unhandled.wav")}, content_type='multipart/form-data')
    # Should hit the generic error branch
    assert resp.status_code in (400, 500)
    data = resp.get_json()
    assert "error" in data

def test_process_audio_final_cleanup_error(client, tmp_path, monkeypatch):
    # Patch to raise AFTER audio is saved, to hit cleanup
    monkeypatch.setattr(audio_processor, "check_audio_quality", lambda f: (True, None))
    def raise_after(*a, **k): raise Exception("fail after save")
    monkeypatch.setattr(audio_processor, "convert_to_wav", raise_after)
    test_file = tmp_path / "fail_cleanup.wav"
    test_file.write_bytes(b"\x00" * 1024)
    with open(test_file, "rb") as f:
        resp = client.post('/process-audio', data={'audio': (f, "fail_cleanup.wav")}, content_type='multipart/form-data')
    assert resp.status_code in (400, 500)
    assert "error" in resp.get_json()

def test_process_audio_os_remove_error(client, tmp_path, monkeypatch):
    monkeypatch.setattr(audio_processor, "check_audio_quality", lambda f: (True, None))
    monkeypatch.setattr(audio_processor, "convert_to_wav", lambda *a, **k: tmp_path / "madeup.wav")
    # Force os.remove to raise
    monkeypatch.setattr(os, "remove", lambda f: (_ for _ in ()).throw(OSError("delete fail")))
    test_file = tmp_path / "test.wav"
    test_file.write_bytes(b"\x00" * 1024)
    with open(test_file, "rb") as f:
        resp = client.post('/process-audio', data={'audio': (f, "test.wav")}, content_type='multipart/form-data')
    assert resp.status_code in (400, 500)
    assert "error" in resp.get_json()

def test_process_audio_final_exception_handler(client, tmp_path, monkeypatch):
    from app.services import audio_processor
    import os
    # Patch check_audio_quality and convert_to_wav to pass and return a temp file
    monkeypatch.setattr(audio_processor, "check_audio_quality", lambda f: (True, None))
    dummy_path = tmp_path / "dummy.wav"
    dummy_path.write_bytes(b"\x00" * 1024)
    monkeypatch.setattr(audio_processor, "convert_to_wav", lambda *a, **k: str(dummy_path))
    # Patch os.remove to throw an error on cleanup, which will get caught by the last except
    monkeypatch.setattr(os, "remove", lambda f: (_ for _ in ()).throw(OSError("remove failed")))
    with open(dummy_path, "rb") as f:
        resp = client.post('/process-audio', data={'audio': (f, "dummy.wav")}, content_type='multipart/form-data')
    assert resp.status_code in (400, 500)
    data = resp.get_json()
    assert "error" in data
    # Optionally check for a log message in stdout/stderr

