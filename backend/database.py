from flask_sqlalchemy import SQLAlchemy
import logging

logger = logging.getLogger(__name__)
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables checked/created successfully.")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            # Depending on your deployment strategy, you might want to exit here
            # sys.exit(1) # Requires 'import sys'