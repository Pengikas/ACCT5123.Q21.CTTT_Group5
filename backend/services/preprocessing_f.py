import json
import os

import joblib
import numpy as np
import pandas as pd

_MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'model')


def _load_pkl(filename):
    return joblib.load(os.path.join(_MODEL_DIR, filename))


def _load_json(filename):
    with open(os.path.join(_MODEL_DIR, filename), encoding='utf-8') as f:
        return json.load(f)


PARAMS = _load_pkl('preprocessing_params.pkl')
METADATA = _load_json('metadata.json')

_feature_file = (
    'feature_names_xgb.pkl'
    if METADATA.get('best_model') == 'XGBoost'
    else 'feature_names_lr.pkl'
)
FEATURE_NAMES = _load_pkl(_feature_file)


def preprocess_employee(employee: dict) -> pd.DataFrame:
    df = pd.DataFrame([employee])

    df['BusinessTravel'] = df['BusinessTravel'].map(PARAMS['travel_map'])
    df['Gender'] = df['Gender'].map(PARAMS['gender_map'])
    df['OverTime'] = df['OverTime'].map(PARAMS['overtime_map'])

    df = pd.get_dummies(df, columns=PARAMS['nominal_cols'], drop_first=True, dtype=int)

    income_q25 = PARAMS['income_q25_train']
    ot = int(df['OverTime'].values[0])

    df['IsYoung'] = (df['Age'] < 30).astype(int)
    df['IsNewHire'] = (df['YearsAtCompany'] < 2).astype(int)
    df['HasStockOption'] = (df['StockOptionLevel'] > 0).astype(int)
    df['IsLowIncome'] = (df['MonthlyIncome'] < income_q25).astype(int)
    df['IsSingle'] = int(df['MaritalStatus_Single'].values[0]) if 'MaritalStatus_Single' in df.columns else 0

    df['OT_LowJobSat'] = int(ot == 1 and df['JobSatisfaction'].values[0] <= 2)
    df['OT_LowEnvSat'] = int(ot == 1 and df['EnvironmentSatisfaction'].values[0] <= 2)
    df['OT_LowWLB'] = int(ot == 1 and df['WorkLifeBalance'].values[0] <= 2)
    df['ManagerStability'] = df['YearsWithCurrManager'] / (df['YearsAtCompany'] + 1)
    df['PromotionGap'] = df['YearsSinceLastPromotion'] / (df['YearsAtCompany'] + 1)
    df['IncomePerYear'] = df['MonthlyIncome'] / (df['TotalWorkingYears'] + 1)

    for col in PARAMS['skewed_features']:
        if col in df.columns:
            df[f'{col}_log'] = np.log1p(df[col])

    df = df.reindex(columns=FEATURE_NAMES, fill_value=0)

    return df
