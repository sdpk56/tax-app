from flask_sqlalchemy import SQLAlchemy
import logging

logger = logging.getLogger(__name__)
db = SQLAlchemy()

def init_db(app):
    """Initialize database and create tables."""
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables checked/created successfully.")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            logger.warning("Continuing with application startup despite database error.")