import unittest
from unittest.mock import patch

from main import ticketdemo


class MockResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


class EventsRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ticketdemo.test_client()

    def test_events_requires_keyword(self):
        response = self.client.get("/events?lat=34.0&lng=-118.2")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "keyword parameter is required")

    def test_events_requires_coordinates(self):
        response = self.client.get("/events?keyword=music")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "lat and lng parameters are required for location",
        )

    @patch("app.services.ticketmaster_client.requests.get")
    def test_events_success_shape(self, mock_get):
        mock_get.return_value = MockResponse(
            200,
            {
                "_embedded": {
                    "events": [
                        {
                            "id": "EVT123",
                            "name": "Sample Event",
                            "url": "https://example.com/event",
                            "dates": {"start": {"dateTime": "2026-01-01T20:00:00Z"}},
                            "images": [{"url": "https://example.com/icon.jpg"}],
                            "classifications": [{"genre": {"name": "Pop"}}],
                            "_embedded": {"venues": [{"name": "Venue A"}]},
                        }
                    ]
                }
            },
        )

        response = self.client.get("/events?keyword=sample&lat=34.0&lng=-118.2")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["event_id"], "EVT123")
        self.assertIn("event_name", data[0])
        self.assertIn("event_url", data[0])
        self.assertIn("genre", data[0])
        self.assertIn("venue", data[0])


if __name__ == "__main__":
    unittest.main()
