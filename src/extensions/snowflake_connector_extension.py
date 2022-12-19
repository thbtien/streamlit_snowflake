from extensions.dynaconf_extension import settings
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import pandas as pd


class SnowflakeConnector:
    def __init__(self) -> None:
        self.engine = create_engine(
            URL(
                account=settings.get("SF_CICD_ACCOUNT"),
                user=settings.get("SF_CICD_USERNAME"),
                password=settings.get("SF_CICD_PASSWORD"),
                database=settings.get("SF_CICD_DATABASE"),
                warehouse=settings.get("SF_CICD_WAREHOUSE"),
                role=settings.get("SF_CICD_ROLE"),
                timezone="Asia/Singapore",
                autocommit=True
                )
            )
        # self.conn = self.engine.connect()

    def get_tables(self, schema):
        query = f"""
            SELECT DISTINCT TABLE_NAME
            FROM INFORMATION_SCHEMA."TABLES"
            WHERE TABLE_SCHEMA = '{schema}'"""
        print(query)
        df = pd.read_sql(query, self.engine)
        return df

    def get_data(self, schema, table):
        df = pd.read_sql_table(table, self.engine, schema=schema, chunksize=200)
        return df