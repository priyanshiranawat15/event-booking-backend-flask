from flask import Blueprint, jsonify, request

from app.exceptions import ApiError
from app.services.venue_service import VenueService
from app.utils.validators import validate_keyword


venues_bp = Blueprint("venues", __name__)


@venues_bp.route("/venues")
def venue_search():
    keyword = request.args.get("keyword")

    keyword_error = validate_keyword(keyword)
    if keyword_error:
        return jsonify({"error": keyword_error}), 400

    try:
        service = VenueService()
        venue = service.find_venue(keyword)
        if not venue:
            return jsonify({"error": "No venues found"}), 404
        return jsonify(venue), 200
    except ApiError as exc:
        return jsonify({"error": exc.message, "status": exc.status_code}), exc.status_code
