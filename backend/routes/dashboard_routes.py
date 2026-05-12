# routes/dashboard_routes.py
from flask import Blueprint, jsonify
import pandas as pd
from database.db_connection import engine
from sqlalchemy import text

dashboard_bp = Blueprint('dashboard_bp', __name__)


@dashboard_bp.route('/dashboard/summary', methods=['GET'])
def dashboard_summary():
    try:
        query = text("""
                     SELECT COUNT(*)                                               as total_employees,
                            SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END)   as high_risk_count,
                            SUM(CASE WHEN risk_level = 'Medium' THEN 1 ELSE 0 END) as medium_risk_count,
                            AVG(probability)                                       as avg_attrition_probability
                     FROM prediction_history
                     """)

        df = pd.read_sql(query, engine)
        result = df.iloc[0].to_dict() if not df.empty else {}

        return jsonify({
            "success": True,
            "data": result
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@dashboard_bp.route('/dashboard/trends', methods=['GET'])
def dashboard_trends():
    try:
        query = text("""
                     SELECT
                         DATE (prediction_time) as prediction_date, COUNT (*) as total_predictions, AVG (probability) as avg_probability
                     FROM prediction_history
                     GROUP BY DATE (prediction_time)
                     ORDER BY prediction_date DESC
                         LIMIT 7
                     """)

        df = pd.read_sql(query, engine)

        return jsonify({
            "success": True,
            "data": df.to_dict(orient='records')
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500