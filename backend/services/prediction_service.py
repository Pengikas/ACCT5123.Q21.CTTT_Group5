# services/prediction_service.py
from services.preprocessing import preprocess_employee
from services.model_service import load_model

def run_prediction(employee):
    model = load_model()
    if model is None:
        return {"success": False, "error": "Model not loaded"}

    processed_input = preprocess_employee(employee)

    # Get probability for Attrition class (class = 1)
    classes = model.classes_

    probabilities = model.predict_proba(
        processed_input
    )[0]

    attrition_index = list(classes).index(1)

    probability = probabilities[attrition_index]
    if probability > 0.7:
        risk_level = "High"
    elif probability >= 0.4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "success": True,
        "attrition_probability": round(float(probability), 3),
        "risk_level": risk_level
    }