# Event Booking (Backend Task) - StagePass API

`StagePass API` is the backend for your `Event Booking (Backend Task)` project.
It is a Flask API that powers an event discovery and booking-oriented experience.
It lets users:
- search nearby events by keyword and location,
- open rich event details,
- fetch venue information such as address, map link, and more events URL.

The backend consumes the Ticketmaster Discovery API and returns clean JSON designed for your frontend (`static/event.html`).

---

## What This Project Does

This project acts as a middle layer between the frontend and Ticketmaster.

Instead of calling Ticketmaster directly from the browser, the frontend calls your Flask endpoints:
- `GET /events` for event list
- `GET /events/<event_id>` for event details
- `GET /venues` for venue details

This gives you one place to:
- validate request inputs,
- transform response payloads into UI-friendly shape,
- centralize API key usage and request handling.

---

## Why This Architecture Is Useful

The codebase is organized to be scalable and easy to maintain:
- `routes` handle HTTP requests/responses
- `services` handle business logic and upstream API calls
- `extractors` format raw upstream data
- `utils` provide reusable helpers (validation, geohash)

This separation makes testing and debugging much easier than a single large `main.py`.

---

## Project Structure

```text
backend/
  app/
    __init__.py               # App factory + blueprint registration
    exceptions.py             # Custom API error class
    routes/
      root.py                 # GET /
      events.py               # GET /events, GET /events/<event_id>
      venues.py               # GET /venues
    services/
      ticketmaster_client.py  # Outbound Ticketmaster HTTP client
      event_service.py        # Event-related business logic
      venue_service.py        # Venue-related business logic
    extractors/
      event_extractor.py      # Event response shaping helpers
      venue_extractor.py      # Venue response shaping helpers
    utils/
      validators.py           # Input validation helpers
      geolocation.py          # Lat/Lng -> geohash converter
  static/
    event.html                # Frontend page
    styles.css
    background.jpg
  tests/
    test_events.py
    test_event_details.py
    test_venues.py
  config.py                   # Env-driven config and constants
  main.py                     # App entrypoint (exports ticketdemo)
  app.yaml                    # App Engine deployment config
  requirements.txt
  requirements-dev.txt
  .env.example
```

---

## Quick Start

### 1. Clone and enter project

```bash
cd /Users/priyanshiranawat/WebTechnologiesAssignments/backend
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Configure environment variables

Create a `.env` file:

```dotenv
TICKETMASTER_API_KEY="YOUR_TICKETMASTER_API_KEY"
REQUEST_TIMEOUT_SECONDS=10
# Optional: CORS_ORIGINS="http://localhost:3000"
```

### 5. Run the server

```bash
python main.py
```

Server default URL:
- `http://127.0.0.1:5000`

---

## How To Use It

### Open the frontend

In browser:
- `http://127.0.0.1:5000/static/event.html`

### Or use API directly

Event search:

```bash
curl "http://127.0.0.1:5000/events?keyword=music&lat=34.0224&lng=-118.2851&distance=10"
```

Event details:

```bash
curl "http://127.0.0.1:5000/events/<event_id>"
```

Venue details:

```bash
curl "http://127.0.0.1:5000/venues?keyword=The%20Wiltern"
```

---

## API Reference

### `GET /`
Purpose: Basic health/status response.

Example response:

```json
{"message":"Hello world!"}
```

### `GET /events`
Query parameters:
- `keyword` (required)
- `lat` (required)
- `lng` (required)
- `distance` (optional, default `10`)
- `category` (optional: `music`, `sports`, `arts`, `film`, `miscellaneous`)

Returns: list of event summaries.

### `GET /events/<event_id>`
Returns: rich event details including date, artist/team, genre, ticket status, seat map, and price range.

### `GET /venues`
Query parameters:
- `keyword` (required)

Returns: venue details including city, address, Google Maps URL, image URL, and more events URL.

---

## Testing

Run all tests:

```bash
pytest -q
```

Current tests cover:
- required-parameter validation
- successful response schema
- event detail normalization behavior

---

## Deployment

Configured for Google App Engine via `app.yaml`.

Key settings:
- runtime: `python311`
- entrypoint: `gunicorn -b :$PORT main:ticketdemo`

`ticketdemo` is intentionally exported in `main.py` for deployment compatibility.

---

## Notes For Contributors

- Keep route contracts stable for frontend compatibility.
- Add logic in `services` and `extractors`, not inside route handlers.
- Add/adjust tests whenever endpoint output changes.
- Keep API keys in environment variables, never hardcoded in source.
