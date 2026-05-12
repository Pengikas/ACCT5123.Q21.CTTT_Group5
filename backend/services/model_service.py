# services/model_service.py
import joblib
from functools import lru_cache
from config import Config

@lru_cache(maxsize=1)
def load_model():
    try:
        model = joblib.load(Config.MODEL_PATH)
        print("Model loaded successfully!")
        return model
    except Exception as e:
        print(f"Failed to load model: {e}")
        return None