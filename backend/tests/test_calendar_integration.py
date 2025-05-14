import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calendar_integration import extract_people, assign_actions_to_people, create_calendar_events

import unittest
from unittest.mock import patch, call

class TestCalendarIntegration(unittest.TestCase):

    def test_extract_people(self):
        text = "Alex and Jordan discussed the plan. Then Sarah joined."
        people = extract_people(text)
        self.assertIn("Alex", people)
        self.assertIn("Jordan", people)
        self.assertIn("Sarah", people)

    def test_assign_actions_to_people(self):
        actions = ["Alex will handle the report.", "Sarah needs to submit the budget."]
        people = ["Alex", "Sarah"]
        assigned = assign_actions_to_people(actions, people)
        self.assertEqual(assigned[0]["owner"], "Alex")
        self.assertEqual(assigned[1]["owner"], "Sarah")

    @patch("calendar_integration.create_calendar_event")
    def test_create_calendar_events(self, mock_create_event):
        actions = [
            {"text": "Finish the website", "owner": "Unassigned"***REMOVED***,
            {"text": "Alex will update the client", "owner": "Alex"***REMOVED***,
        ]
        create_calendar_events(actions)
        self.assertEqual(mock_create_event.call_count, 2)
        calls = [call_args[0][0] for call_args in mock_create_event.call_args_list]
        self.assertIn("Meeting Follow-up", calls)
        self.assertIn("Follow-up: Alex", calls)

if __name__ == '__main__':
    unittest.main()
