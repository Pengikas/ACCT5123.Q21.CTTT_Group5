# backend/routes/employee_routes.py

from flask import Blueprint
from flask import jsonify

import pandas as pd

from sqlalchemy import text

from backend.database.db_connection import engine

employee_bp = Blueprint(
    "employee_bp",
    __name__
)

# ====================================
# GET ALL EMPLOYEES
# ====================================

@employee_bp.route(
    "/employees",
    methods=["GET"]
)
def get_employees():

    try:

        query = text("""

            SELECT

                EmployeeNumber,

                employee_name,

                Department,

                JobRole,

                email,

                Age,

                MonthlyIncome,

                YearsAtCompany,

                JobSatisfaction,

                EnvironmentSatisfaction,

                Attrition

            FROM employees

            ORDER BY EmployeeNumber DESC

        """)

        df = pd.read_sql(
            query,
            engine
        )

        # risk label

        def get_risk(attrition):

            if attrition == "Yes":

                return "High"

            return "Low"

        df["risk_level"] = (

            df["Attrition"]

            .apply(get_risk)
        )

        return jsonify({

            "success": True,

            "count": len(df),

            "employees":

                df.to_dict(
                    orient="records"
                )

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ====================================
# GET EMPLOYEE DETAIL
# ====================================

@employee_bp.route(
    "/employees/<int:employee_id>",
    methods=["GET"]
)
def get_employee_detail(employee_id):

    try:

        query = text("""

            SELECT *

            FROM employees

            WHERE EmployeeNumber = :emp_id

        """)

        df = pd.read_sql(

            query,

            engine,

            params={
                "emp_id": employee_id
            }
        )

        if df.empty:

            return jsonify({

                "success": False,

                "error": "Employee not found"

            }), 404

        employee = df.iloc[0].to_dict()

        employee["risk_level"] = (

            "High"

            if employee["Attrition"] == "Yes"

            else "Low"
        )

        return jsonify({

            "success": True,

            "data": employee

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500