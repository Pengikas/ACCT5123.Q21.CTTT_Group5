# services/database_service.py
from sqlalchemy import text
from database.db_connection import engine
import pandas as pd

def get_employee_by_id(employee_id):
    query = text("SELECT * FROM employees WHERE employee_id = :emp_id")
    df = pd.read_sql(query, engine, params={"emp_id": employee_id})
    return df.iloc[0].to_dict() if not df.empty else None


def save_prediction(employee_id, probability, risk_level):
    query = text("""
        INSERT INTO prediction_history 
        (employee_id, probability, risk_level, prediction_time)
        VALUES (:emp_id, :prob, :risk, NOW())
    """)
    with engine.connect() as conn:
        conn.execute(query, {
            "emp_id": employee_id,
            "prob": float(probability),
            "risk": risk_level
        })
        conn.commit()