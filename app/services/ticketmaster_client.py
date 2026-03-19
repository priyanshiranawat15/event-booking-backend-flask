import requests
from flask import current_app

from app.exceptions import ApiError


class TicketmasterClient:
    def __init__(self):
        self.api_key = current_app.config["API_KEY"]
        self.timeout = current_app.config["REQUEST_TIMEOUT_SECONDS"]

    def _request(self, url, params):
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
        except requests.RequestException as exc:
            raise ApiError(f"Failed to fetch data from upstream: {exc}", 502) from exc

        if response.status_code != 200:
            raise ApiError("Failed to fetch upstream data", response.status_code)

        return response.json()

    def search_events(self, keyword, geo_point, distance, segment_id=None):
        params = {
            "apikey": self.api_key,
            "keyword": keyword,
            "geoPoint": geo_point,
            "radius": str(distance),
            "unit": "miles",
        }
        if segment_id:
            params["segmentId"] = segment_id

        return self._request(current_app.config["BASE_URL"], params)

    def get_event_details(self, event_id):
        url = f"{current_app.config['EVENT_DETAILS_URL']}/{event_id}"
        params = {"apikey": self.api_key}
        return self._request(url, params)

    def search_venues(self, keyword):
        params = {"apikey": self.api_key, "keyword": keyword}
        return self._request(current_app.config["VENUE_SEARCH_URL"], params)
