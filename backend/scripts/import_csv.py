from sqlalchemy import create_engine
from backend.config import Config

import pandas as pd
import random

from faker import Faker

fake = Faker()

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI
)

# load dataset
df = pd.read_csv(
    "data/final/final_ml_dataset.csv"
)

departments = [
    "Engineering",
    "HR",
    "Finance",
    "Marketing",
    "Sales",
    "Operations"
]

job_roles = {
    "Engineering": [
        "Software Engineer",
        "Data Engineer",
        "Backend Developer"
    ],

    "HR": [
        "HR Specialist",
        "Recruiter"
    ],

    "Finance": [
        "Financial Analyst",
        "Accountant"
    ],

    "Marketing": [
        "Marketing Specialist",
        "SEO Executive"
    ],

    "Sales": [
        "Sales Executive",
        "Business Development"
    ],

    "Operations": [
        "Operations Analyst",
        "Project Coordinator"
    ]
}

# generate fake info (ERP)

employee_names = []
employee_departments = []
employee_roles = []
employee_emails = []

for _ in range(len(df)):

    name = fake.name()

    dept = random.choice(departments)

    role = random.choice(job_roles[dept])

    email = (
        name.lower()
        .replace(" ", ".")
        + "@gmail.com"
    )

    employee_names.append(name)
    employee_departments.append(dept)
    employee_roles.append(role)
    employee_emails.append(email)

# add columns
df["employee_name"] = employee_names
df["department"] = employee_departments
df["job_role"] = employee_roles
df["email"] = employee_emails

# save to mysql
df.to_sql(
    name="employees",
    con=engine,
    if_exists="append",
    index=False
)

print("CSV imported successfully!")
