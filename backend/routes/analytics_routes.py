# routes/analytics_routes.py

from flask import Blueprint, jsonify
from backend.services.model_service import load_model
import joblib
import os

analytics_bp = Blueprint('analytics_bp', __name__)
# load exact feature order used during training
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

top_cols_path = os.path.join(
    BASE_DIR,
    "model",
    "feature_names_lr.pkl"
)

TOP_COLS = joblib.load(top_cols_path)


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
