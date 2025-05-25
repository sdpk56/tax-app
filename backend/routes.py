from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from database import db
from tax_calculator import calculate_tax
import logging

logger = logging.getLogger(__name__)
routes = Blueprint("routes", __name__)

@routes.route("/calculate-tax", methods=["POST"])
@jwt_required()
def tax():
    data = request.get_json()
    if not data:
        logger.warning("Tax calculation attempt with no JSON data.")
        return jsonify({"message": "No input data provided"}), 400

    income = data.get("income")
    regime = data.get("regime")

    # Input validation
    if income is None or not isinstance(income, (int, float)):
        logger.warning(f"Invalid income type received: {type(income)}")
        return jsonify({"message": "Income must be a valid number."}), 400
    if income < 0:
        logger.warning(f"Negative income received: {income}")
        return jsonify({"message": "Income cannot be negative."}), 400

    if not isinstance(regime, str) or regime not in ["old", "new"]:
        logger.warning(f"Invalid tax regime received: {regime}")
        return jsonify({"message": "Tax regime must be 'old' or 'new'."}), 400

    try:
        tax_amount = calculate_tax(income, regime)
        logger.info(f"Tax calculated for user {get_jwt_identity()}: income={income}, regime={regime}, tax={tax_amount}")
        return jsonify({"income": income, "regime": regime, "tax": tax_amount}), 200
    except Exception as e:
        logger.error(f"Error during tax calculation for user {get_jwt_identity()}: {e}")
        return jsonify({"message": "An error occurred during tax calculation."}), 500

@routes.route("/user-info", methods=["GET"])
@jwt_required()
def user_info():
    current_user_identity = get_jwt_identity()
    user = User.query.filter_by(username=current_user_identity).first()
    if user:
        logger.info(f"User info requested for: {current_user_identity}")
        return jsonify({"username": user.username}), 200
    else:
        logger.error(f"User not found for identity: {current_user_identity}")
        return jsonify({"message": "User not found."}), 404