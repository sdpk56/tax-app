import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS # Import CORS
from dotenv import load_dotenv # Import load_dotenv
import logging # Import logging

# Load environment variables from .env file for local development
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from database import db, init_db
from auth import auth
from routes import routes
from config import Config # Import Config

app = Flask(__name__)

# Load configuration from Config object
app.config.from_object(Config)

# Initialize JWT
jwt = JWTManager(app)

# Initialize SQLAlchemy DB
init_db(app)

# Enable CORS for all routes (adjust origins as needed for production)
CORS(app, resources={r"/*": {"origins": "*"}})
# For production, you might want to specify allowed origins:
# CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "https://your-frontend-domain.com"]}})


# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(routes)

# JWT Error Handlers
@jwt.unauthorized_loader
def unauthorized_response(callback):
    logger.warning("Unauthorized access attempt.")
    return jsonify({"message": "Missing Authorization Header"}), 401

@jwt.invalid_token_loader
def invalid_token_response(callback):
    logger.warning("Invalid token received.")
    return jsonify({"message": "Signature verification failed"}), 403

@jwt.expired_token_loader
def expired_token_response(callback):
    logger.warning("Expired token received.")
    return jsonify({"message": "Token has expired"}), 401

@jwt.revoked_token_loader
def revoked_token_response(callback):
    logger.warning("Revoked token received.")
    return jsonify({"message": "Token has been revoked"}), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_response(callback):
    logger.warning("Fresh token required.")
    return jsonify({"message": "Fresh token required"}), 401


if __name__ == "__main__":
    # In development, you can run with Flask's built-in server
    # In production, Gunicorn will be used (configured in docker-compose.yml)
    if app.config.get('FLASK_ENV') == 'development':
        logger.info("Starting Flask development server...")
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        logger.info("Running in production mode (Gunicorn will serve the app).")
        # This block won't be executed when run via Gunicorn in Docker
        # It's here for completeness if you were to run app.py directly in a prod-like env