# backend/routes/dashboard_routes.py

from flask import Blueprint
from flask import jsonify

import pandas as pd

from sqlalchemy import text

from backend.database.db_connection import engine

dashboard_bp = Blueprint(
    "dashboard_bp",
    __name__
)

# ====================================
# DASHBOARD SUMMARY
# ====================================

@dashboard_bp.route(
    "/dashboard/summary",
    methods=["GET"]
)
def dashboard_summary():

    try:

        query = text("""

            SELECT

                COUNT(*) as total_employees,

                SUM(
                    CASE
                        WHEN Attrition = 'Yes'
                        THEN 1
                        ELSE 0
                    END
                ) as high_risk_count

            FROM employees

        """)

        df = pd.read_sql(
            query,
            engine
        )

        result = (
            df.iloc[0].to_dict()
            if not df.empty
            else {}
        )

        total_employees = result.get(
            "total_employees",
            0
        )

        high_risk_count = result.get(
            "high_risk_count",
            0
        )

        attrition_rate = 0

        if total_employees > 0:

            attrition_rate = round(

                (
                    high_risk_count
                    / total_employees
                ) * 100,

                2
            )

        return jsonify({

            "success": True,

            "total_employees":
                int(total_employees),

            "high_risk_count":
                int(high_risk_count),

            "attrition_rate":
                attrition_rate

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ====================================
# DASHBOARD TRENDS
# ====================================

@dashboard_bp.route(
    "/dashboard/trends",
    methods=["GET"]
)
def dashboard_trends():

    try:

        query = text("""

            SELECT

                Department,

                COUNT(*) as total_employees,

                SUM(
                    CASE
                        WHEN Attrition = 'Yes'
                        THEN 1
                        ELSE 0
                    END
                ) as attrition_count

            FROM employees

            GROUP BY Department

            ORDER BY attrition_count DESC

        """)

        df = pd.read_sql(
            query,
            engine
        )

        return jsonify({

            "success": True,

            "data":

                df.to_dict(
                    orient="records"
                )

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500