# python
# File: streamlit/streamlit_app.py
import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://aff_admin:affina_poOB7G9A51@172.16.10.32:3306/profiling_analysis?charset=utf8mb4")
engine = create_engine(DATABASE_URL)

st.title("Custom Streamlit Dashboard")

@st.cache_data
def load_sample(limit=500):
    query = f"SELECT * FROM raw_data LIMIT {limit}"
    return pd.read_sql(query, engine)

df = load_sample()
st.write("Rows:", len(df))
st.dataframe(df)

# quick chart if numeric column exists
numeric_cols = df.select_dtypes("number").columns.tolist()
if numeric_cols:
    col = st.selectbox("Numeric column", numeric_cols)
    st.line_chart(df[col])
else:
    st.info("No numeric columns found for charting.")
