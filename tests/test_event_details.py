import unittest
from unittest.mock import patch

from main import ticketdemo


class MockResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


class EventDetailsRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ticketdemo.test_client()

    @patch("app.services.ticketmaster_client.requests.get")
    def test_event_details_normalizes_missing_values(self, mock_get):
        mock_get.return_value = MockResponse(
            200,
            {
                "id": "EVT1",
                "name": "Minimal Event",
                "dates": {
                    "start": {"localDate": "2026-03-10"},
                    "status": {"code": "onsale"},
                },
            },
        )

        response = self.client.get("/events/EVT1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertEqual(data["event_id"], "EVT1")
        self.assertEqual(data["event_name"], "Minimal Event")
        self.assertEqual(data["price_range"], "N/A")
        self.assertEqual(data["ticket_status"], "onsale")
        self.assertEqual(data["artist_team"], "N/A")
        self.assertEqual(data["venue"], "N/A")


if __name__ == "__main__":
    unittest.main()
