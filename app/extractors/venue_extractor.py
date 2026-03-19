import urllib.parse


def extract_venue_details(venue_data):
    venue_info = {
        "name": venue_data.get("name", "N/A"),
        "city": "N/A",
        "address": "N/A",
        "google_maps_url": "N/A",
        "venue_image_url": "N/A",
        "more_events_url": "N/A",
    }
    if venue_data.get("url"):
        venue_info["more_events_url"] = venue_data["url"]

    city_parts = []
    if "city" in venue_data and "name" in venue_data["city"]:
        city_parts.append(venue_data["city"]["name"])
    if "state" in venue_data and "name" in venue_data["state"]:
        city_parts.append(venue_data["state"]["name"])

    if city_parts:
        venue_info["city"] = ", ".join(city_parts)

    if "address" in venue_data and "line1" in venue_data["address"]:
        venue_info["address"] = venue_data["address"]["line1"]

    if "images" in venue_data and venue_data["images"]:
        venue_info["venue_image_url"] = venue_data["images"][0].get("url", "N/A")

    maps_components = []
    if venue_info["name"] != "N/A":
        maps_components.append(venue_info["name"])
    if venue_info["address"] != "N/A":
        maps_components.append(venue_info["address"])
    if "city" in venue_data and "name" in venue_data["city"]:
        maps_components.append(venue_data["city"]["name"])
    if "state" in venue_data and "name" in venue_data["state"]:
        maps_components.append(venue_data["state"]["name"])
    if "postalCode" in venue_data:
        maps_components.append(venue_data["postalCode"])

    if maps_components:
        maps_query = ", ".join(maps_components)
        encoded_query = urllib.parse.quote(maps_query)
        venue_info["google_maps_url"] = (
            f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        )

    return venue_info
