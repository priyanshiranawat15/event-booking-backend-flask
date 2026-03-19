import os


class Config:
    API_KEY = os.getenv("TICKETMASTER_API_KEY", "INSERT YOUR API KEY HERE")
    BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
    EVENT_DETAILS_URL = "https://app.ticketmaster.com/discovery/v2/events"
    VENUE_SEARCH_URL = "https://app.ticketmaster.com/discovery/v2/venues"

    CATEGORY = {
        "music": "KZFzniwnSyZfZ7v7nJ",
        "sports": "KZFzniwnSyZfZ7v7nE",
        "arts": "KZFzniwnSyZfZ7v7nA",
        "film": "KZFzniwnSyZfZ7v7nn",
        "miscellaneous": "KZFzniwnSyZfZ7v7n1",
    }

    # Comma-separated list in env; empty means allow all (current behavior).
    _cors_origins = os.getenv("CORS_ORIGINS", "")
    CORS_ORIGINS = [o.strip() for o in _cors_origins.split(",") if o.strip()] or None

    REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
