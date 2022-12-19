from extensions.snowpark_extension import Snowpark
from snowflake.snowpark.functions import col
import streamlit as st

def load_data():
    snow = Snowpark()
    df = snow.session.table("TRACKER") \
            .select(["BORROWER_NAME", "UEN", "POSTMAN_ID", "STATUS", "MANUALLY_OVERRIDE", "MODIFIED_AT"])
    borrower_name = df[["BORROWER_NAME"]] 
    borrower_selected = st.multiselect(
        "Borrower Name",
        borrower_name
    )

    if len(borrower_selected) == 0:
        filtered_df = df
    else:
        filtered_df = df.filter(col("BORROWER_NAME").isin(st.session_state["borrower_selected"]))

    st.dataframe(filtered_df, use_container_width=True)

with st.container():
    st.subheader("Tracker list")
    load_data()