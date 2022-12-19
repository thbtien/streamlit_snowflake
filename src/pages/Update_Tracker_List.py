from extensions.snowpark_extension import Snowpark
from snowflake.snowpark.functions import when_matched, when_not_matched
import streamlit as st
import pandas as pd


@st.cache
def convert_df(df: pd.DataFrame):
    return df.to_csv(index=False).encode("utf-8")


file_upload = st.file_uploader("Choose a file")
if file_upload is not None:
    if file_upload.name.endswith(".xlsx"):
        xl = pd.ExcelFile(file_upload.getvalue())
        sheet_name = st.selectbox(
            "Select sheet",
            xl.sheet_names
        )
        df = xl.parse(sheet_name)
        df
        # df.sheet_names
    if file_upload.name.endswith(".csv"):
        df = pd.read_csv(file_upload)

    if st.button("Save data"):
        snow = Snowpark()
        snow.session.use_schema("PUBLIC")
        src_df = snow.session.create_dataframe(df)
        target_df = snow.session.table("TRACKER")
        target_df.merge(
            src_df, 
            target_df["UEN"] == src_df["UEN"],
            [
                when_matched().update(
                    {
                        "STATUS": src_df["STATUS"],
                        "MANUALLY_OVERRIDE": True
                    }
                ),
                when_not_matched().insert(
                    {
                        "BORROWER_NAME": src_df["BORROWER_NAME"],
                        "UEN": src_df["UEN"],
                        "POSTMAN_ID": src_df["POSTMAN_ID"],
                        "STATUS": src_df["STATUS"],
                        "MANUALLY_OVERRIDE": False,
                    }
                )
            ]
        )
        target_df.collect()
        # df.write.mode("overwrite").save_as_table("TEMP_TRACKER")
        # df.to_sql("TEMP_TRACKER", snow.session)
        # query = """MERGE INTO TRACKER t USING TEMP_TRACKER tt 
        #     ON t.UEN = tt.UEN
        #     WHEN MATCHED THEN 
        #         UPDATE SET t.STATUS = tt.STATUS,
        #             t.MANUALLY_OVERRIDE = TRUE
        #     WHEN NOT MATCHED THEN
        #         INSERT (BORROWER_NAME, UEN, POSTMAN_ID, STATUS, MANUALLY_OVERRIDE) VALUES (tt.BORROWER_NAME, tt.UEN, tt.POSTMAN_ID, tt.STATUS, FALSE)"""
        # snow.session.query(query)
        # query = "DROP TABLE TEMP_TRACKER"
        # snow.session.query(query)

    