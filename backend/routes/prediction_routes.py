from flask import Blueprint
from flask import jsonify
from flask import request

from backend.services.prediction_service import (
    run_prediction
)

from backend.services.database_service import (
    get_employee_by_id
)

prediction_bp = Blueprint(
    "prediction",
    __name__
)

# ====================================
# Predict Existing Employee
# ====================================

@prediction_bp.route(
    "/predict/<int:employee_id>",
    methods=["POST"]
)
def predict_employee(employee_id):

    try:

        employee = get_employee_by_id(
            employee_id
        )

        if not employee:

            return jsonify({
                "success": False,
                "error": "Employee not found"
            }), 404

        result = run_prediction(
            employee
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ====================================
# Manual Prediction
# ====================================

@prediction_bp.route(
    "/predict/manual",
    methods=["POST"]
)
def predict_manual():

    try:

        employee_data = request.json

        result = run_prediction(
            employee_data
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500