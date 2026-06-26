"""Entry point for the HELIX application.

Sets up logging, loads configuration, registers blueprints, and validates
the MongoDB connection on startup.
"""

import logging
from flask import Flask, render_template
from config import Config
from backend.utils.logger import setup_logging
from backend.database.mongo import MongoConnection
from backend.api.dashboard import dashboard_bp
from backend.api.events import events_bp
from backend.api.analytics import analytics_bp
from backend.api.search import search_bp

# Set up global logging config
setup_logging()
logger = logging.getLogger(__name__)

def create_app() -> Flask:
    """Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    logger.info("Initializing HELIX Flask application...")
    
    app_instance = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )
    app_instance.config.from_object(Config)

    # Serve the dashboard UI on the root path
    @app_instance.route("/", methods=["GET"])
    def index() -> str:
        return render_template("index.html")

    # Register blueprints
    app_instance.register_blueprint(dashboard_bp, url_prefix="/api")
    app_instance.register_blueprint(events_bp, url_prefix="/api")
    app_instance.register_blueprint(analytics_bp, url_prefix="/api")
    app_instance.register_blueprint(search_bp, url_prefix="/api")
    logger.info("Flask Blueprints registered successfully under prefix /api.")

    # Validate MongoDB connection
    db_connected = False
    try:
        MongoConnection.get_client()
        logger.info("MongoDB startup connection check succeeded.")
        db_connected = True
    except ConnectionError as err:
        logger.error("MongoDB is unavailable on startup: %s. Application will continue in degraded mode.", err)
    except Exception as err:
        logger.error("Unexpected error connecting to MongoDB on startup: %s", err)

    # Initialize and start Scheduler if database connection is available
    if db_connected:
        import os
        if not app_instance.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            try:
                from backend.scheduler.scheduler import start_scheduler
                start_scheduler()
            except Exception as err:
                logger.error("Failed to start background scheduler on startup: %s", err)
    else:
        logger.warning("Scheduler startup bypassed due to missing MongoDB connection.")

    return app_instance

# Expose app for WSGI servers
app = create_app()

if __name__ == "__main__":
    logger.info("Starting HELIX dev server...")
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
