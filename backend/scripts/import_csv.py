from sqlalchemy import create_engine
from backend.config import Config
import pandas as pd

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI
)

df = pd.read_csv(
    "data/final/final_ml_dataset.csv"
)

df.to_sql(
    name="employees",
    con=engine,
    if_exists="append",
    index=False
)

print("CSV imported successfully!")