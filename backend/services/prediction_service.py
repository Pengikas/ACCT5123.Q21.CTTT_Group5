# backend/services/prediction_service.py

from backend.services.preprocessing import (
    preprocess_employee
)

from backend.services.model_service import (
    load_model,
    get_preprocessing_params
)

# ====================================
# LOAD PARAMS
# ====================================

PARAMS = get_preprocessing_params()

THRESHOLD = PARAMS[
    "threshold_recommended"
]

# ====================================
# RUN PREDICTION
# ====================================

def run_prediction(employee):

    try:

        # load trained model

        model = load_model()

        if model is None:

            return {

                "success": False,

                "error":
                    "Model could not be loaded"
            }

        # preprocess raw employee input

        processed_input = preprocess_employee(
            employee
        )

        # get attrition probability

        probability = (

            model.predict_proba(
                processed_input
            )[0][1]

        )

        # risk classification

        if probability >= THRESHOLD:

            risk_level = "High"

        elif probability >= 0.5:

            risk_level = "Medium"

        else:

            risk_level = "Low"

        return {

            "success": True,

            "attrition_probability":

                round(
                    float(probability),
                    4
                ),

            "risk_level":
                risk_level,

            "threshold_used":
                THRESHOLD
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }