from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db
import logging

logger = logging.getLogger(__name__)
auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() # Use get_json() for robustness
    if not data:
        logger.warning("Signup attempt with no JSON data.")
        return jsonify({"message": "No input data provided"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        logger.warning("Signup attempt with missing username or password.")
        return jsonify({"message": "Username and password are required"}), 400

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        logger.info(f"Signup attempt for existing username: {username}")
        return jsonify({"message": "Username already exists. Please choose a different one."}), 409 # Conflict

    try:
        # Hash the password before storing it
        # Use a stronger method if available, e.g., 'pbkdf2:sha256:260000' for more iterations
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        logger.info(f"User '{username}' registered successfully.")
        return jsonify({"message": "User registered successfully!"}), 201 # Created
    except Exception as e:
        db.session.rollback() # Rollback in case of error
        logger.error(f"Error during user registration for '{username}': {e}")
        return jsonify({"message": "An error occurred during registration."}), 500

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        logger.warning("Login attempt with no JSON data.")
        return jsonify({"message": "No input data provided"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        logger.warning("Login attempt with missing username or password.")
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # Set expires_delta to a specific time, e.g., 30 minutes
        # from datetime import timedelta
        # access_token = create_access_token(identity=user.username, expires_delta=timedelta(minutes=30))
        access_token = create_access_token(identity=user.username) # Using default expiration from config
        logger.info(f"User '{username}' logged in successfully.")
        return jsonify({"access_token": access_token}), 200
    else:
        logger.info(f"Failed login attempt for username: {username}")
        return jsonify({"message": "Invalid username or password"}), 401 # More specific error message