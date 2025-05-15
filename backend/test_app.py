import unittest
from unittest.mock import patch
from run import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_no_audio_upload(self):
        response = self.app.post('/process-audio', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("No file uploaded", response.get_data(as_text=True))

    def test_invalid_json_to_process_json(self):
        response = self.app.post('/process-json', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], "Transcript is empty or missing.")
    
    @patch("run.create_calendar_event")
    @patch("run.generate_summary_and_extraction")
    def test_process_json_with_sample(self, mock_generate, mock_create_meeting):
        mock_generate.return_value = {
            "summary": ["Mock summary"],
            "actions": ["Mock action item"],
            "decisions": ["Mock decision"]
        }
        mock_create_meeting.return_value = {
            "status": "success",
            "meeting_url": "https://mock.zoho.meeting"
        }

        sample = {"transcript": "We decided to launch next week. John will prepare slides."}
        response = self.app.post('/process-json', json=sample)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("summary", data)
        self.assertIn("actions", data)
        self.assertIn("decisions", data)


if __name__ == '__main__':
    unittest.main()

