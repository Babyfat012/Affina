# python
# File: ingest/ingest.py
import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://babyfat:admin@postgres:5432/analytics")
ENGINE = create_engine(DATABASE_URL)

def load_excel(path="data.xlsx", sheet=0):
    df = pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
    return df

def clean(df):
    # minimal cleaning example
    df = df.drop_duplicates()
    df = df.dropna(how="all")
    # cast columns, rename, parse dates etc.
    return df

def main():
    df = load_excel("data.xlsx")
    df = clean(df)
    # write to Postgres; table name example: raw_data
    df.to_sql("raw_data", ENGINE, if_exists="replace", index=False)
    print("Ingest finished: wrote", len(df), "rows")

if __name__ == "__main__":
    main()
