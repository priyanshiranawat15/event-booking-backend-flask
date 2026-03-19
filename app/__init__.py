from flask import Flask
from flask_cors import CORS

from config import Config


def create_app(config_class=Config):
    # Serve static assets from the existing top-level ./static directory.
    app = Flask(__name__, static_folder="../static", static_url_path="/static")
    app.config.from_object(config_class)

    # Keep current behavior: allow all origins unless configured.
    cors_origins = app.config.get("CORS_ORIGINS")
    if cors_origins:
        CORS(app, resources={r"/*": {"origins": cors_origins}})
    else:
        CORS(app)

    from app.routes.events import events_bp
    from app.routes.root import root_bp
    from app.routes.venues import venues_bp

    app.register_blueprint(root_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(venues_bp)

    return app
