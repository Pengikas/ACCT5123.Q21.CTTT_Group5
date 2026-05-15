# routes/employee_routes.py

from flask import Blueprint, jsonify
import pandas as pd
from database.db_connection import engine
from sqlalchemy import text

employee_bp = Blueprint('employee_bp', __name__)


@employee_bp.route('/employees', methods=['GET'])
def get_employees():

    try:

        query = text("""

            SELECT
                employee_id,
                employee_name,
                department,
                job_role,
                Age,
                YearsAtCompany,
                MonthlyIncome,
                WorkStress,
                SatisfactionIndex,
                Attrition

            FROM employees

            ORDER BY employee_id DESC

        """)

        df = pd.read_sql(query, engine)

        # risk labels
        def get_risk(attrition):

            if attrition == 1:
                return "High"

            return "Low"

        df["risk_level"] = df["Attrition"].apply(get_risk)

        return jsonify({
            "success": True,
            "count": len(df),
            "data": df.to_dict(orient='records')
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@employee_bp.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee_detail(employee_id):

    try:

        query = text("""

            SELECT *
            FROM employees
            WHERE employee_id = :emp_id

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

        # ERP display values
        employee["risk_level"] = (
            "High"
            if employee["Attrition"] == 1
            else "Low"
        )

        employee["work_stress_label"] = (
            "High"
            if employee["WorkStress"] >= 3
            else "Normal"
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