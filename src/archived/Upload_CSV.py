import streamlit as st
from extensions.snowflake_connector_extension import SnowflakeConnector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd

def load_csv_to_snowflake():
    file_upload = st.file_uploader("Choose a file")
    # table = st.text_input("Table name", "None")
    snow = SnowflakeConnector()
    snow.engine.execute("USE SCHEMA PUBLIC")
    if "public_tables" not in st.session_state:
        st.session_state.public_tables = snow.get_tables("PUBLIC")
    if file_upload is not None:
        col1, col2 = st.columns(2)
        with col1:
            table = st.selectbox(
                "Select table",
                st.session_state.public_tables
            )
        with col2:
            insert_mode = st.radio(
                "Insert mode",
                ("Append", "Replace")
            )
        
        if st.button("Save data"):
            df = pd.read_csv(file_upload)
            df.to_sql(table.lower(), snow.engine, if_exists=insert_mode.lower(), index=False)
            "Data loaded successfully"

st.set_page_config(
    page_title="Load csv to snowflake"
)
st.markdown("# Upload CSV to Snowflake")
st.sidebar.header("Upload csv")
"This page for uploading data from csv files to snowflake"

load_csv_to_snowflake()