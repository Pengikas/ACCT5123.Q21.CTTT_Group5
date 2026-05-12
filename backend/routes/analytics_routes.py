# routes/analytics_routes.py

from flask import Blueprint, jsonify
from services.model_service import load_model
import joblib

analytics_bp = Blueprint('analytics_bp', __name__)

TOP_COLS = joblib.load("../model/top_cols.pkl")


@analytics_bp.route('/analytics/feature-importance', methods=['GET'])
def feature_importance():

    try:

        model = load_model()

        if model is None:
            return jsonify({
                "success": False,
                "error": "Model not loaded"
            }), 500

        importances = model.feature_importances_

        importance_list = sorted([
            {
                "feature": name,
                "importance": round(float(imp), 4)
            }
            for name, imp in zip(TOP_COLS, importances)
        ], key=lambda x: x["importance"], reverse=True)

        return jsonify({
            "success": True,
            "data": importance_list
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
