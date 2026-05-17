from sqlalchemy import create_engine

from backend.config import Config

import os

import pandas as pd

from faker import Faker

fake = Faker()

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI
)

# ====================================
# LOAD DATASET
# ====================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

csv_path = os.path.join(
    BASE_DIR,
    "data",
    "WA_Fn-UseC_-HR-Employee-Attrition.csv"
)

df = pd.read_csv(csv_path)

# ====================================
# GENERATE ERP FIELDS
# ====================================

employee_names = []

employee_emails = []

for _ in range(len(df)):

    name = fake.name()

    email = (

        name.lower()

        .replace(" ", ".")

        + "@gmail.com"
    )

    employee_names.append(name)

    employee_emails.append(email)

# ====================================
# ADD ERP COLUMNS
# ====================================

df["employee_name"] = (
    employee_names
)

df["email"] = (
    employee_emails
)

# ====================================
# SAVE TO MYSQL
# ====================================

df.to_sql(

    name="employees",

    con=engine,

    if_exists="replace",

    index=False
)

print(
    "CSV imported successfully!"
)