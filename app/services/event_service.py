from flask import current_app

from app.extractors.event_extractor import map_event_details, map_event_summary
from app.services.ticketmaster_client import TicketmasterClient
from app.utils.geolocation import convert_to_geohash


class EventService:
    def __init__(self):
        self.client = TicketmasterClient()

    def search_events(self, keyword, lat, lng, category, distance):
        geo_point = convert_to_geohash(lat, lng)
        segment_id = None

        categories = current_app.config["CATEGORY"]
        if category and category in categories:
            segment_id = categories[category]

        data = self.client.search_events(
            keyword=keyword,
            geo_point=geo_point,
            distance=distance,
            segment_id=segment_id,
        )

        events = []
        if "_embedded" in data and "events" in data["_embedded"]:
            for event in data["_embedded"]["events"]:
                events.append(map_event_summary(event))

        return events

    def get_event_details(self, event_id):
        data = self.client.get_event_details(event_id)
        return map_event_details(data)
