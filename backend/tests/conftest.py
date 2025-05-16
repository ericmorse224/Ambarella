import pytest
import os

@pytest.fixture(scope='session')
def test_audio_file():
    return "tests/sample_audio.wav"