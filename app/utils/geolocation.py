import geohash


def convert_to_geohash(lat, lng):
    """Convert latitude and longitude to geohash with precision 7."""
    return geohash.encode(lat, lng, 7)
