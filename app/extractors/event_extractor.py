from datetime import datetime


def extract_date_time(event_data):
    if "dates" not in event_data or "start" not in event_data["dates"]:
        return None

    start_data = event_data["dates"]["start"]
    date_part = start_data.get("localDate", "")
    time_part = start_data.get("localTime", "")

    if date_part and time_part:
        return f"{date_part} {time_part}"
    if date_part:
        return date_part
    return None


def extract_ticket_status(event_data):
    if "dates" not in event_data or "status" not in event_data["dates"]:
        return None

    status = event_data["dates"]["status"]
    return status.get("code")


def extract_artists_teams(event_data):
    if "_embedded" not in event_data or "attractions" not in event_data["_embedded"]:
        return None

    attractions = event_data["_embedded"]["attractions"]
    names = []
    for attraction in attractions:
        if "name" in attraction:
            name = attraction["name"]
            url = attraction.get("url")
            href = (
                f'<a href="{url}" target="_blank" '
                "onclick=\"window.open(this.href, 'artistWindow', 'width=1024,height=768,scrollbars=yes,resizable=yes,menubar=no,toolbar=no,location=no,status=no'); return false;\" "
                f'rel="noopener noreferrer">{name}</a>'
                if url
                else name
            )
            names.append(href)

    return " | ".join(names) if names else None


def extract_venue_name(event_data):
    if "_embedded" not in event_data or "venues" not in event_data["_embedded"]:
        return None

    venues = event_data["_embedded"]["venues"]
    if venues and "name" in venues[0]:
        return venues[0]["name"]
    return None


def extract_genre_info(event_data):
    if "classifications" not in event_data or not event_data["classifications"]:
        return None

    classification = event_data["classifications"][0]
    genre_parts = []

    for field in ["subGenre", "genre", "segment", "subType", "type"]:
        if field in classification and classification[field] and "name" in classification[field]:
            genre_parts.append(classification[field]["name"])

    return " | ".join(genre_parts) if genre_parts else None


def extract_urls(event_data):
    urls = {}
    if "url" in event_data:
        urls["buy_ticket_at"] = event_data["url"]

    if "seatmap" in event_data and "staticUrl" in event_data["seatmap"]:
        urls["seat_map"] = event_data["seatmap"]["staticUrl"]

    return urls


def map_event_summary(event):
    event_data = {
        "event_id": event.get("id"),
        "date": None,
        "icon": None,
        "event_name": event.get("name"),
        "event_url": event.get("url"),
        "genre": None,
        "venue": None,
    }

    if "dates" in event and "start" in event["dates"]:
        if "dateTime" in event["dates"]["start"]:
            event_data["date"] = event["dates"]["start"]["dateTime"]
        elif "localDate" in event["dates"]["start"]:
            date_str = event["dates"]["start"]["localDate"]
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                event_data["date"] = date_obj.isoformat()
            except ValueError:
                event_data["date"] = date_str

    if "images" in event and event["images"]:
        for image in event["images"]:
            if image.get("url"):
                event_data["icon"] = image["url"]
                break

    if "classifications" in event and event["classifications"]:
        classification = event["classifications"][0]
        if "genre" in classification and classification["genre"].get("name"):
            event_data["genre"] = classification["genre"]["name"]

    if "_embedded" in event and "venues" in event["_embedded"] and event["_embedded"]["venues"]:
        venue = event["_embedded"]["venues"][0]
        event_data["venue"] = venue.get("name")

    return event_data


def map_event_details(event_data):
    details = {
        "date": extract_date_time(event_data),
        "artist_team": extract_artists_teams(event_data),
        "venue": extract_venue_name(event_data),
        "genre": extract_genre_info(event_data),
        "ticket_status": extract_ticket_status(event_data),
        "event_name": event_data.get("name"),
        "event_id": event_data.get("id"),
        "seat_map": event_data.get("seatmap", {}).get("staticUrl"),
    }

    details.update(extract_urls(event_data))

    if "images" in event_data and event_data["images"]:
        details["image"] = event_data["images"][0].get("url")

    if "priceRanges" in event_data and event_data["priceRanges"]:
        price_range = event_data["priceRanges"][0]
        if "min" in price_range and "max" in price_range:
            details["price_range"] = f"${price_range['min']} - ${price_range['max']}"
        elif "min" in price_range:
            details["price_range"] = f"From ${price_range['min']}"
        else:
            details["price_range"] = "N/A"
    else:
        details["price_range"] = "N/A"

    return {k: v if v is not None else "N/A" for k, v in details.items()}
