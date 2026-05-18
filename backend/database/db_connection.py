# database/db_connection.py
from sqlalchemy import create_engine
from backend.config import Config

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)