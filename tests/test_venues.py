import unittest
from unittest.mock import patch

from main import ticketdemo


class MockResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


class VenueRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.client = ticketdemo.test_client()

    def test_venues_requires_keyword(self):
        response = self.client.get("/venues")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "keyword parameter is required")

    @patch("app.services.ticketmaster_client.requests.get")
    def test_venues_not_found(self, mock_get):
        mock_get.return_value = MockResponse(200, {"_embedded": {"venues": []}})
        response = self.client.get("/venues?keyword=test")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "No venues found")

    @patch("app.services.ticketmaster_client.requests.get")
    def test_venues_success_schema(self, mock_get):
        mock_get.return_value = MockResponse(
            200,
            {
                "_embedded": {
                    "venues": [
                        {
                            "name": "Venue A",
                            "city": {"name": "Los Angeles"},
                            "state": {"name": "CA"},
                            "address": {"line1": "123 Main St"},
                            "postalCode": "90001",
                            "images": [{"url": "https://example.com/venue.jpg"}],
                            "url": "https://example.com/more",
                        }
                    ]
                }
            },
        )

        response = self.client.get("/venues?keyword=venue")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn("name", data)
        self.assertIn("city", data)
        self.assertIn("address", data)
        self.assertIn("google_maps_url", data)
        self.assertIn("venue_image_url", data)
        self.assertIn("more_events_url", data)


if __name__ == "__main__":
    unittest.main()
