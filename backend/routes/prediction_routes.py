# routes/prediction_routes.py
from flask import Blueprint, jsonify
from services.database_service import get_employee_by_id, save_prediction
from services.prediction_service import run_prediction

prediction_bp = Blueprint('prediction_bp', __name__)


@prediction_bp.route('/predict/<int:employee_id>', methods=['POST'])
def predict_employee(employee_id):
    try:
        employee = get_employee_by_id(employee_id)

        if employee is None:
            return jsonify({
                "success": False,
                "error": "Employee not found"
            }), 404

        result = run_prediction(employee)

        if not result["success"]:
            return jsonify(result), 400

        save_prediction(
            employee_id,
            result["attrition_probability"],
            result["risk_level"]
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500