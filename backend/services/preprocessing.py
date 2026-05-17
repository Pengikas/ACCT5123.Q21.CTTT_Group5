# backend/services/preprocessing.py

import pandas as pd
import numpy as np

from backend.services.model_service import (
    get_top_cols,
    get_preprocessing_params
)

# ====================================
# LOAD TRAINING ARTIFACTS
# ====================================

TOP_COLS = get_top_cols()

PARAMS = get_preprocessing_params()

travel_map = PARAMS["travel_map"]

overtime_map = PARAMS["overtime_map"]

gender_map = PARAMS["gender_map"]

income_q25_train = PARAMS[
    "income_q25_train"
]

nominal_cols = PARAMS[
    "nominal_cols"
]

skewed_features = PARAMS[
    "skewed_features"
]

# ====================================
# REQUIRED INPUT FIELDS
# ====================================

required_fields = [

    "Age",
    "MonthlyIncome",
    "TotalWorkingYears",
    "DailyRate",
    "YearsAtCompany",
    "YearsWithCurrManager",

    "BusinessTravel",
    "Gender",
    "OverTime",

    "DistanceFromHome",
    "StockOptionLevel",
    "NumCompaniesWorked",

    "JobLevel",
    "YearsInCurrentRole",

    "EnvironmentSatisfaction",
    "JobSatisfaction",
    "JobInvolvement",

    "TrainingTimesLastYear",
    "YearsSinceLastPromotion",
    "RelationshipSatisfaction",

    "Department",
    "EducationField",
    "JobRole",
    "MaritalStatus",

    "WorkLifeBalance"
]

# ====================================
# VALIDATION
# ====================================

def validate_employee_input(employee):

    missing_fields = []

    for field in required_fields:

        if (

            field not in employee

            or

            employee[field] in [None, ""]

        ):

            missing_fields.append(field)

    if missing_fields:

        raise ValueError(
            f"Missing required fields: {missing_fields}"
        )

    # ====================================
    # BASIC NUMERIC VALIDATION
    # ====================================

    if employee["Age"] <= 0:

        raise ValueError(
            "Age must be greater than 0"
        )

    if employee["MonthlyIncome"] <= 0:

        raise ValueError(
            "MonthlyIncome must be greater than 0"
        )

    if employee["TotalWorkingYears"] < 0:

        raise ValueError(
            "TotalWorkingYears cannot be negative"
        )

    if employee["YearsAtCompany"] < 0:

        raise ValueError(
            "YearsAtCompany cannot be negative"
        )

# ====================================
# MAIN PREPROCESSING
# ====================================

def preprocess_employee(employee):

    # validate raw input

    validate_employee_input(employee)

    # convert to dataframe

    df = pd.DataFrame([employee])

    # ====================================
    # REMOVE TARGET COLUMN
    # ====================================

    if "Attrition" in df.columns:

        df = df.drop(
            columns=["Attrition"]
        )

    # ====================================
    # SAFE ENCODING
    # ====================================

    # BusinessTravel

    if str(df["BusinessTravel"].dtype) == "object":

        df["BusinessTravel"] = (

            df["BusinessTravel"]

            .map(travel_map)

        )

    # Gender

    if str(df["Gender"].dtype) == "object":

        df["Gender"] = (

            df["Gender"]

            .map(gender_map)

        )

    # OverTime

    if str(df["OverTime"].dtype) == "object":

        df["OverTime"] = (

            df["OverTime"]

            .map(overtime_map)

        )

    # ====================================
    # ONE HOT ENCODING
    # ====================================

    df = pd.get_dummies(

        df,

        columns=nominal_cols,

        drop_first=True,

        dtype=int
    )

    # ====================================
    # FEATURE ENGINEERING
    # ====================================

    # binary features

    df["IsYoung"] = (

        df["Age"] < 30

    ).astype(int)

    df["IsNewHire"] = (

        df["YearsAtCompany"] < 2

    ).astype(int)

    df["HasStockOption"] = (

        df["StockOptionLevel"] > 0

    ).astype(int)

    df["IsLowIncome"] = (

        df["MonthlyIncome"] < income_q25_train

    ).astype(int)

    # marital status

    if "MaritalStatus_Single" in df.columns:

        df["IsSingle"] = (

            df["MaritalStatus_Single"]

        )

    else:

        df["IsSingle"] = 0

    # ====================================
    # INTERACTION FEATURES
    # ====================================

    df["OT_LowJobSat"] = (

        (

            df["OverTime"] == 1

        )

        &

        (

            df["JobSatisfaction"] <= 2

        )

    ).astype(int)

    df["OT_LowEnvSat"] = (

        (

            df["OverTime"] == 1

        )

        &

        (

            df["EnvironmentSatisfaction"] <= 2

        )

    ).astype(int)

    df["OT_LowWLB"] = (

        (

            df["OverTime"] == 1

        )

        &

        (

            df["WorkLifeBalance"] <= 2

        )

    ).astype(int)

    # ====================================
    # RATIO FEATURES
    # ====================================

    df["ManagerStability"] = (

        df["YearsWithCurrManager"]

        /

        (

            df["YearsAtCompany"] + 1

        )

    )

    df["PromotionGap"] = (

        df["YearsSinceLastPromotion"]

        /

        (

            df["YearsAtCompany"] + 1

        )

    )

    df["IncomePerYear"] = (

        df["MonthlyIncome"]

        /

        (

            df["TotalWorkingYears"] + 1

        )

    )

    # ====================================
    # LOG TRANSFORMATION
    # ====================================

    for col in skewed_features:

        # prevent negative values

        df[col] = df[col].clip(
            lower=0
        )

        df[f"{col}_log"] = np.log1p(
            df[col]
        )

    # ====================================
    # FEATURE ALIGNMENT
    # ====================================

    # add missing columns
    # from training feature space

    for col in TOP_COLS:

        if col not in df.columns:

            df[col] = 0

    # exact training order

    df = df[TOP_COLS]

    # ====================================
    # FINAL CLEANUP
    # ====================================

    # force numeric types

    df = df.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # remove NaN

    df = df.fillna(0)

    return df