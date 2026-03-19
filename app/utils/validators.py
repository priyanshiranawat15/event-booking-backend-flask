def validate_keyword(keyword):
    if not keyword:
        return "keyword parameter is required"
    return None


def validate_coordinates(lat, lng):
    if not lat or not lng:
        return None, None, "lat and lng parameters are required for location"

    try:
        return float(lat), float(lng), None
    except ValueError:
        return None, None, "lat and lng must be valid numbers"


def normalize_distance(distance):
    return distance if distance else "10"


def normalize_category(category):
    return category.lower() if category else ""
