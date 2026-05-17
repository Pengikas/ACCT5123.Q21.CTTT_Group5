# backend/services/database_service.py

import pandas as pd

from sqlalchemy import text

from backend.database.db_connection import engine

# ====================================
# GET EMPLOYEE BY ID
# ====================================

def get_employee_by_id(employee_id):

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

            return None

        employee = (
            df.iloc[0]
            .to_dict()
        )

        return employee

    except Exception as e:

        print(
            f"Database error: {e}"
        )

        return None


# ====================================
# GET ALL EMPLOYEES
# ====================================

def get_all_employees():

    try:

        query = text("""

            SELECT *

            FROM employees

        """)

        df = pd.read_sql(
            query,
            engine
        )

        return (
            df.to_dict(
                orient="records"
            )
        )

    except Exception as e:
        print(
            f"Database error: {e}"
        )
        return []
