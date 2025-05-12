import unittest
from run import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_no_audio_upload(self):
        response = self.app.post('/process-audio', data={***REMOVED***)
        self.assertEqual(response.status_code, 400)
        self.assertIn("No file uploaded", response.get_data(as_text=True))

    def test_invalid_json_to_process_json(self):
        response = self.app.post('/process-json', json={***REMOVED***)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], "Transcript is empty or missing.")


    def test_process_json_with_sample(self):
        sample = {"transcript": "We decided to launch next week. John will prepare slides."***REMOVED***
        response = self.app.post('/process-json', json=sample)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("decisions", data)
        self.assertIn("actions", data)
        self.assertIn("summary", data)

if __name__ == '__main__':
    unittest.main()
