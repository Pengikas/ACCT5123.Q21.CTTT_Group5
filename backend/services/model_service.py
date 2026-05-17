import os
import joblib

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)

# ====================================
# PATHS
# ====================================

BEST_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "best_model.pkl"
)

FEATURES_PATH = os.path.join(
    MODEL_DIR,
    "feature_names_lr.pkl"
)

PREPROCESSING_PARAMS_PATH = os.path.join(
    MODEL_DIR,
    "preprocessing_params.pkl"
)

# ====================================
# LOAD ARTIFACTS
# ====================================

MODEL = joblib.load(
    BEST_MODEL_PATH
)

TOP_COLS = joblib.load(
    FEATURES_PATH
)

PREPROCESSING_PARAMS = joblib.load(
    PREPROCESSING_PARAMS_PATH
)


def load_model():

    return MODEL


def get_top_cols():

    return TOP_COLS


def get_preprocessing_params():

    return PREPROCESSING_PARAMS