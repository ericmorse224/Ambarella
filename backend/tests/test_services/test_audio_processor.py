import os
import pytest
from app.services import audio_processor
import subprocess

def test_convert_to_wav_invalid_file():
    with pytest.raises(Exception):
        audio_processor.convert_to_wav("not_a_real_file.mp3")

def test_trim_silence_bad_input():
    with pytest.raises(Exception):
        audio_processor.trim_silence("nonexistent.wav")

def test_transcribe_audio_invalid_path():
    with pytest.raises(Exception):
        audio_processor.transcribe_audio("not_a_real_file.wav")

def test_get_audio_duration_error(monkeypatch):
    # Patch subprocess.run to raise
    monkeypatch.setattr("subprocess.run", lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))
    assert audio_processor.get_audio_duration("nofile.wav") == -1

def test_get_sample_rate_channels_error(monkeypatch):
    monkeypatch.setattr("subprocess.run", lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))
    assert audio_processor.get_sample_rate_channels("nofile.wav") == (0, 0)

def test_get_bitrate_error(monkeypatch):
    monkeypatch.setattr("subprocess.run", lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))
    assert audio_processor.get_bitrate("nofile.wav") == 0

def test_get_rms_volume_error(monkeypatch):
    monkeypatch.setattr("subprocess.run", lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))
    assert audio_processor.get_rms_volume("nofile.wav") is None

def test_get_silence_ratio_error(monkeypatch):
    monkeypatch.setattr("subprocess.run", lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))
    assert audio_processor.get_silence_ratio("nofile.wav") == 1.0

def test_check_audio_quality_all_errors(tmp_path, monkeypatch):
    file_path = str(tmp_path / "dummy.mp3")
    # Not exist
    ok, msg = audio_processor.check_audio_quality(file_path)
    assert not ok and "does not exist" in msg

    # Unsupported format
    bad_file = str(tmp_path / "bad.txt")
    with open(bad_file, "w") as f:
        f.write("data")
    ok, msg = audio_processor.check_audio_quality(bad_file)
    assert not ok and "Unsupported" in msg

    # Patch all helpers to trigger error/low-quality branches
    realfile = str(tmp_path / "dummy.wav")
    with open(realfile, "wb") as f:
        f.write(b"\0")
    monkeypatch.setattr(audio_processor, "is_supported_format", lambda p: True)
    monkeypatch.setattr(audio_processor, "get_audio_duration", lambda p: -1)
    ok, msg = audio_processor.check_audio_quality(realfile)
    assert not ok and "Unable to determine" in msg

    monkeypatch.setattr(audio_processor, "get_audio_duration", lambda p: 1.0)
    ok, msg = audio_processor.check_audio_quality(realfile)
    assert not ok and "too short" in msg

    monkeypatch.setattr(audio_processor, "get_audio_duration", lambda p: 1e7)
    ok, msg = audio_processor.check_audio_quality(realfile)
    assert not ok and "too long" in msg

    monkeypatch.setattr(audio_processor, "get_audio_duration", lambda p: 10.0)
    monkeypatch.setattr(audio_processor, "get_sample_rate_channels", lambda p: (8000, 1))
    ok, msg = audio_processor.check_audio_quality(realfile)
    assert not ok and "Sample rate too low" in msg

    monkeypatch.setattr(audio_processor, "get_sample_rate_channels", lambda p: (16000, 1))
    monkeypatch.setattr(audio_processor, "get_bitrate", lambda p: 10000)
    ok, msg = audio_processor.check_audio_quality(realfile)
    assert not ok and "Bitrate too low" in msg

    monkeypatch.setattr(audio_processor, "get_bitrate", lambda p: 32000)
    monkeypatch.setattr(audio_processor, "get_rms_volume", lambda p: -50.0)
    ok, msg = audio_processor.check_audio_quality(realfile)
    assert not ok and "Audio too quiet" in msg

    monkeypatch.setattr(audio_processor, "get_rms_volume", lambda p: -10.0)
    monkeypatch.setattr(audio_processor, "get_silence_ratio", lambda p: 0.7)
    ok, msg = audio_processor.check_audio_quality(realfile)
    assert not ok and "Audio too silent" in msg

    # Success path
    monkeypatch.setattr(audio_processor, "get_silence_ratio", lambda p: 0.1)
    ok, msg = audio_processor.check_audio_quality(realfile)
    assert ok and msg == "OK"

def test_convert_to_wav_raises(monkeypatch):
    # Patch subprocess.run to raise CalledProcessError
    class DummyException(Exception): pass
    def raise_err(*a, **k): raise DummyException("ffmpeg fail")
    monkeypatch.setattr("subprocess.run", raise_err)
    with pytest.raises(DummyException):
        audio_processor.convert_to_wav("input.mp3", "output.wav")

def test_trim_silence_fails(monkeypatch):
    import subprocess
    def raise_err(*a, **k): raise subprocess.CalledProcessError(1, "cmd")
    monkeypatch.setattr("subprocess.run", raise_err)
    assert not audio_processor.trim_silence("a.wav", "b.wav")

# Test get_sample_rate_channels with malformed output
def test_get_sample_rate_channels_malformed(monkeypatch):
    class DummyResult:
        stdout = "not,a,number"
    monkeypatch.setattr("subprocess.run", lambda *a, **k: DummyResult())
    assert audio_processor.get_sample_rate_channels("dummy.wav") == (0, 0)

# Test get_audio_duration with malformed output
def test_get_audio_duration_malformed(monkeypatch):
    class DummyResult:
        stdout = "notanumber"
    monkeypatch.setattr("subprocess.run", lambda *a, **k: DummyResult())
    assert audio_processor.get_audio_duration("dummy.wav") == -1

# Test convert_to_wav returning bad/empty output file
def test_convert_to_wav_empty_output(tmp_path, monkeypatch):
    def dummy_run(*a, **k): return
    monkeypatch.setattr("subprocess.run", dummy_run)
    input_file = tmp_path / "test.mp3"
    input_file.write_bytes(b"\x00" * 1024)
    output_file = tmp_path / "test.wav"
    out = audio_processor.convert_to_wav(str(input_file), str(output_file))
    assert out is None


# Test trim_silence with missing output file
def test_trim_silence_failure(tmp_path, monkeypatch):
    import subprocess
    # Patch subprocess.run to raise
    monkeypatch.setattr("subprocess.run", lambda *a, **k: (_ for _ in ()).throw(subprocess.CalledProcessError(1, "ffmpeg")))
    input_file = tmp_path / "test.wav"
    input_file.write_bytes(b"\x00" * 1024)
    result = audio_processor.trim_silence(str(input_file), "should_fail.wav")
    assert not result

def test_get_sample_rate_channels_malformed(monkeypatch):
    # Malformed output, triggers ValueError (lines 82, 85)
    class DummyResult:
        stdout = "foo"
    monkeypatch.setattr("subprocess.run", lambda *a, **k: DummyResult())
    sr, ch = audio_processor.get_sample_rate_channels("dummy.wav")
    assert sr == 0 and ch == 0

def test_convert_to_wav_no_output_file(tmp_path, monkeypatch):
    # subprocess.run does not raise, but output file is missing (line 109)
    def dummy_run(*a, **k): return None
    monkeypatch.setattr("subprocess.run", dummy_run)
    input_file = tmp_path / "file.mp3"
    input_file.write_bytes(b"\x00" * 1024)
    output_file = tmp_path / "output.wav"
    result = audio_processor.convert_to_wav(str(input_file), str(output_file))
    assert result is None

def test_convert_to_wav_raises(tmp_path, monkeypatch):
    def raise_err(*a, **k): raise subprocess.CalledProcessError(1, "ffmpeg")
    monkeypatch.setattr("app.services.audio_processor.subprocess.run", raise_err)
    input_file = tmp_path / "fail.mp3"
    input_file.write_bytes(b"\x00" * 1024)
    output_file = tmp_path / "fail.wav"
    with pytest.raises(subprocess.CalledProcessError):
        audio_processor.convert_to_wav(str(input_file), str(output_file))
