from app.extractors.venue_extractor import extract_venue_details
from app.services.ticketmaster_client import TicketmasterClient


class VenueService:
    def __init__(self):
        self.client = TicketmasterClient()

    def find_venue(self, keyword):
        data = self.client.search_venues(keyword)

        venues_list = []
        if "_embedded" in data and "venues" in data["_embedded"]:
            for venue in data["_embedded"]["venues"]:
                venues_list.append(extract_venue_details(venue))

        return venues_list[0] if venues_list else None
