# services/preprocessing.py

import pandas as pd
import joblib

# load exact feature order used during training
TOP_COLS = joblib.load("../model/top_cols.pkl")


def preprocess_employee(employee):

    overtime_map = {
        "Yes": 1,
        "No": 0
    }

    overtime = overtime_map.get(employee.get("OverTime"), 0)

    work_life_balance = employee.get("WorkLifeBalance")

    environment_satisfaction = employee.get("EnvironmentSatisfaction")
    job_satisfaction = employee.get("JobSatisfaction")
    relationship_satisfaction = employee.get("RelationshipSatisfaction")

    # feature enrich

    work_stress = overtime * (4 - work_life_balance)

    satisfaction_index = (
        environment_satisfaction +
        job_satisfaction +
        relationship_satisfaction
    ) / 3

    data = {
        "MonthlyIncome": employee.get("MonthlyIncome"),
        "Age": employee.get("Age"),
        "TotalWorkingYears": employee.get("TotalWorkingYears"),
        "DailyRate": employee.get("DailyRate"),
        "YearsAtCompany": employee.get("YearsAtCompany"),
        "YearsWithCurrManager": employee.get("YearsWithCurrManager"),

        "SatisfactionIndex": satisfaction_index,

        "OverTime": overtime,

        "DistanceFromHome": employee.get("DistanceFromHome"),
        "StockOptionLevel": employee.get("StockOptionLevel"),
        "NumCompaniesWorked": employee.get("NumCompaniesWorked"),

        "WorkStress": work_stress,

        "JobLevel": employee.get("JobLevel"),
        "YearsInCurrentRole": employee.get("YearsInCurrentRole"),

        "EnvironmentSatisfaction": environment_satisfaction,
        "JobSatisfaction": job_satisfaction,
        "JobInvolvement": employee.get("JobInvolvement"),

        "TrainingTimesLastYear": employee.get("TrainingTimesLastYear"),
        "YearsSinceLastPromotion": employee.get("YearsSinceLastPromotion"),
        "RelationshipSatisfaction": relationship_satisfaction,
    }

    df = pd.DataFrame([data])

    # IMPORTANT:
    # force exact feature order used during training
    df = df[TOP_COLS]

    return df


def preprocess_dataframe(df):

    overtime_map = {
        "Yes": 1,
        "No": 0
    }

    # encode
    df["OverTime"] = df["OverTime"].map(overtime_map)

    # feature engineering
    df["WorkStress"] = (
        df["OverTime"] *
        (4 - df["WorkLifeBalance"])
    )

    df["SatisfactionIndex"] = (
        df["EnvironmentSatisfaction"] +
        df["JobSatisfaction"] +
        df["RelationshipSatisfaction"]
    ) / 3

    # select exact training columns
    df = df[TOP_COLS]

    return df

