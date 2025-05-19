import nltk
import os
import pytest
from app import create_app
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

@pytest.fixture(scope='session', autouse=True)
def setup_nltk_data():
    nltk_data_dir = os.path.join(os.path.expanduser("~"), "nltk_data")
    if not os.path.exists(nltk_data_dir):
        os.makedirs(nltk_data_dir)
    nltk.data.path.append(nltk_data_dir)
    nltk.download('punkt', download_dir=nltk_data_dir)
    nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_dir)
    nltk.download('maxent_ne_chunker', download_dir=nltk_data_dir)
    nltk.download('words', download_dir=nltk_data_dir)

@pytest.fixture(scope='session')
def test_audio_file():
    return "tests/sample_audio.wav"

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client