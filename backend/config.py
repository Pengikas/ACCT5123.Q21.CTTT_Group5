# config.py
from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.urandom(32)
    DEBUG = os.getenv("DEBUG", "True").lower() in ["true", "1", "yes"]

    # Database
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    # Model
    MODEL_PATH = "model/model.pkl"