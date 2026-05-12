# routes/report_routes.py
from flask import Blueprint, jsonify

report_bp = Blueprint('report_bp', __name__)


@report_bp.route('/reports/export', methods=['GET'])
def export_report():
    try:

        return jsonify({
            "success": True,
            "message": "Report exported successfully (demo)"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500