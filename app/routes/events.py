from flask import Blueprint, jsonify, request

from app.exceptions import ApiError
from app.services.event_service import EventService
from app.utils.validators import (
    normalize_category,
    normalize_distance,
    validate_coordinates,
    validate_keyword,
)


events_bp = Blueprint("events", __name__)


@events_bp.route("/events")
def events():
    keyword = request.args.get("keyword")
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    keyword_error = validate_keyword(keyword)
    if keyword_error:
        return jsonify({"error": keyword_error}), 400

    lat, lng, coord_error = validate_coordinates(lat, lng)
    if coord_error:
        return jsonify({"error": coord_error}), 400

    distance = normalize_distance(request.args.get("distance", "10"))
    category = normalize_category(request.args.get("category", ""))

    try:
        service = EventService()
        events_list = service.search_events(keyword, lat, lng, category, distance)
        return jsonify(events_list)
    except ApiError as exc:
        return jsonify({"error": exc.message, "status": exc.status_code}), exc.status_code


@events_bp.route("/events/<event_id>")
def event_details(event_id):
    if not event_id:
        return jsonify({"error": "Event ID is required"}), 400

    try:
        service = EventService()
        details = service.get_event_details(event_id)
        return jsonify(details)
    except ApiError as exc:
        return jsonify({"error": exc.message, "status": exc.status_code}), exc.status_code
