import streamlit as st
from extensions.snowflake_connector_extension import SnowflakeConnector
import pandas as pd


@st.cache
def convert_df(df: pd.DataFrame):
    return df.to_csv(index=False).encode("utf-8")


st.markdown("# Get Finance data from Snowflake")
schema = "FINANCE_DATAMART"
snow = SnowflakeConnector()

if "tables" not in st.session_state:
    st.session_state.tables = snow.get_tables(schema)
table = st.selectbox(
    "Select table",
    st.session_state.tables
)

if st.button("Get data"):
    # df = snow.get_data(schema, table)
    df = pd.DataFrame(snow.engine.execute(f"SELECT * FROM {schema}.{table}").fetchall())
    df

    st.download_button(
        "Download data as csv",
        data=convert_df(df),
        file_name=f"{table}.csv",
        mime="text/csv"
    )

