from extensions.snowpark_extension import Snowpark
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd


@st.cache
def convert_df(df: pd.DataFrame):
    return df.to_csv(index=False).encode("utf-8")

snow = Snowpark()

df = snow.session.table("ETB_DATABASE.DATAMART_ETB_CUSTOMER_SUMMARY").to_pandas()
cust_name = df["CUST_NAME"].sort_values().to_list()
# df
with st.container():
    st.subheader("Customer summary data")
    customer_name = st.multiselect(
        "Customer Name",
        ["All"] + cust_name
    )
    if customer_name == "All":
        filter_df = df.head(20)
    else:
        filter_df = df.loc[df["CUST_NAME"] == customer_name]
    filter_df
    chart = filter_df[["CUST_NAME", "DPD_5_TIMES"]]
    st.bar_chart(
        chart,
        x="CUST_NAME",
        y="DPD_5_TIMES")
    st.download_button(
        "Download data as csv",
        data=convert_df(filter_df),
        file_name=f"Customer summary data.csv",
        mime="text/csv"
    )