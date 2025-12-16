from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, TaxCalculation
from database import db
from tax_calculator import calculate_tax, compare_tax_regimes, calculate_tax_slabs_breakdown
import logging

logger = logging.getLogger(__name__)
routes = Blueprint("routes", __name__)

# Marker log for CI/AI PR review testing
logger.debug("ai_pr_review: routes module loaded (test marker)")

@routes.route("/calculate-tax", methods=["POST"])
@jwt_required()
def tax() -> tuple:
    """Calculate tax with optional deductions and rebates."""
    data = request.get_json()
    if not data:
        logger.warning("Tax calculation attempt with no JSON data.")
        return jsonify({"message": "No input data provided"}), 400

    income = data.get("income")
    regime = data.get("regime")
    deductions = data.get("deductions", 0)
    rebates = data.get("rebates", {})
    save_history = data.get("save_history", True)

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
        tax_result = calculate_tax(income, regime, deductions, rebates)
        
        # Save to history if requested
        if save_history:
            current_user_identity = get_jwt_identity()
            user = User.query.filter_by(username=current_user_identity).first()
            if user:
                calculation = TaxCalculation(
                    user_id=user.id,
                    gross_income=tax_result['gross_income'],
                    deductions=tax_result['deductions'],
                    taxable_income=tax_result['taxable_income'],
                    base_tax=tax_result['base_tax'],
                    surcharge=tax_result['surcharge'],
                    health_education_cess=tax_result['health_education_cess'],
                    total_tax=tax_result['total_tax'],
                    effective_tax_rate=tax_result['effective_tax_rate'],
                    regime=regime,
                    take_home_annual=tax_result['take_home_annual'],
                    take_home_monthly=tax_result['take_home_monthly']
                )
                db.session.add(calculation)
                db.session.commit()
        
        logger.info(f"Tax calculated for user {get_jwt_identity()}: income={income}, regime={regime}, tax={tax_result['total_tax']}")
        return jsonify(tax_result), 200
    except Exception as e:
        logger.error(f"Error during tax calculation for user {get_jwt_identity()}: {e}")
        return jsonify({"message": "An error occurred during tax calculation."}), 500


@routes.route("/compare-regimes", methods=["POST"])
@jwt_required()
def compare_regimes() -> tuple:
    """Compare tax liability between old and new regimes."""
    data = request.get_json()
    if not data:
        logger.warning("Regime comparison attempt with no JSON data.")
        return jsonify({"message": "No input data provided"}), 400

    income = data.get("income")
    deductions = data.get("deductions", 0)

    if income is None or not isinstance(income, (int, float)) or income < 0:
        logger.warning(f"Invalid income for comparison: {income}")
        return jsonify({"message": "Income must be a valid non-negative number."}), 400

    try:
        comparison = compare_tax_regimes(income, deductions)
        logger.info(f"Tax regimes compared for user {get_jwt_identity()}: income={income}")
        return jsonify(comparison), 200
    except Exception as e:
        logger.error(f"Error during regime comparison: {e}")
        return jsonify({"message": "An error occurred during comparison."}), 500


@routes.route("/tax-slabs/<regime>", methods=["GET"])
@jwt_required()
def get_tax_slabs(regime: str) -> tuple:
    """Get detailed tax slab breakdown."""
    income = request.args.get("income", type=float)
    
    if income is None or income < 0:
        logger.warning(f"Invalid income for slab breakdown: {income}")
        return jsonify({"message": "Income must be a valid non-negative number."}), 400
    
    if regime not in ["old", "new"]:
        logger.warning(f"Invalid tax regime: {regime}")
        return jsonify({"message": "Tax regime must be 'old' or 'new'."}), 400

    try:
        breakdown = calculate_tax_slabs_breakdown(income, regime)
        logger.info(f"Tax slab breakdown generated for user {get_jwt_identity()}: income={income}, regime={regime}")
        return jsonify({"regime": regime, "income": income, "slabs": breakdown}), 200
    except Exception as e:
        logger.error(f"Error generating slab breakdown: {e}")
        return jsonify({"message": "An error occurred while generating slab breakdown."}), 500


@routes.route("/tax-history", methods=["GET"])
@jwt_required()
def tax_history() -> tuple:
    """Get user's tax calculation history."""
    current_user_identity = get_jwt_identity()
    user = User.query.filter_by(username=current_user_identity).first()
    
    if not user:
        logger.error(f"User not found: {current_user_identity}")
        return jsonify({"message": "User not found."}), 404
    
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        calculations = TaxCalculation.query.filter_by(user_id=user.id)\
            .order_by(TaxCalculation.created_at.desc())\
            .paginate(page=page, per_page=per_page)
        
        logger.info(f"Tax history retrieved for user {current_user_identity}")
        return jsonify({
            'total': calculations.total,
            'pages': calculations.pages,
            'current_page': page,
            'calculations': [calc.to_dict() for calc in calculations.items]
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving tax history: {e}")
        return jsonify({"message": "An error occurred while retrieving history."}), 500


@routes.route("/tax-history/<int:calc_id>", methods=["DELETE"])
@jwt_required()
def delete_tax_calculation(calc_id: int) -> tuple:
    """Delete a specific tax calculation from history."""
    current_user_identity = get_jwt_identity()
    user = User.query.filter_by(username=current_user_identity).first()
    
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    try:
        calculation = TaxCalculation.query.filter_by(id=calc_id, user_id=user.id).first()
        if not calculation:
            return jsonify({"message": "Calculation not found."}), 404
        
        db.session.delete(calculation)
        db.session.commit()
        logger.info(f"Tax calculation deleted for user {current_user_identity}: calc_id={calc_id}")
        return jsonify({"message": "Calculation deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting tax calculation: {e}")
        return jsonify({"message": "An error occurred while deleting calculation."}), 500


@routes.route("/user-info", methods=["GET"])
@jwt_required()
def user_info() -> tuple:
    """Get current user information."""
    current_user_identity = get_jwt_identity()
    user = User.query.filter_by(username=current_user_identity).first()
    if user:
        logger.info(f"User info requested for: {current_user_identity}")
        return jsonify({"username": user.username, "created_at": user.created_at.isoformat()}), 200
    else:
        logger.error(f"User not found for identity: {current_user_identity}")
        return jsonify({"message": "User not found."}), 404