import streamlit as st
from extensions.snowflake_connector_extension import SnowflakeConnector
from extensions.snowpark_extension import Snowpark
import pandas as pd
from snowflake.snowpark.functions import col, sum, lower, date_trunc, cast


snow_conn = SnowflakeConnector()
query = """SELECT 
    INVESTOR_ID,
    TO_DATE(DEPOSITED_DATE_1) AS DEPOSITED_DATE_1,
    SUM(AMOUNT_DEPOSITED) AS AMOUNT_DEPOSITED
FROM SNAPSHOT_DATABASE.CURATED_INVESTOR_FUND_TRANSACTION
WHERE AMOUNT_DEPOSITED > 0
    AND LOWER(LOAN_TRANSACTION_DESCRIPTION) IN ('deposit', 'referral fee', 'commission rebate', 'internal')
GROUP BY INVESTOR_ID, TO_DATE(DEPOSITED_DATE_1)"""
snow_conn_df = pd.read_sql(query, snow_conn.engine)


snowpark = Snowpark()
# snowpark_df = snowpark.session.sql(query)
snowpark_df = snowpark.session.table("SNAPSHOT_DATABASE.CURATED_INVESTOR_FUND_TRANSACTION") \
    .filter(col("IT_IS_INSURED") == 0 ) \
    .filter(lower(col("LOAN_TRANSACTION_DESCRIPTION")).isin("withdrawal", "internal")) \
    .select( col("INVESTOR_ID"), cast(col("AMOUNT_WITHDRAWN"), "DOUBLE").alias("AMOUNT_WITHDRAWN"), date_trunc("MONTH", col("DATE_WITHDRAWAL")).alias("DATE_WITHDRAWAL") )
    
snowpark_df = snowpark_df.group_by(["DATE_WITHDRAWAL", "INVESTOR_ID"]).sum("AMOUNT_WITHDRAWN").alias("AMOUNT_WITHDRAWN")

col1, col2 = st.columns(2)

with col1:
    snow_conn_df

with col2:
    snowpark_df
