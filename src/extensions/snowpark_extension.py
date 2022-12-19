import os
from snowflake.snowpark.session import Session
import pandas as pd
from extensions.dynaconf_extension import settings

class Snowpark:
    def __init__(self) -> None:
        self.conn = {
            "account": settings.get("SF_CICD_ACCOUNT"),
            "user": settings.get("SF_CICD_USERNAME"),
            "password": settings.get("SF_CICD_PASSWORD"),
            "role": settings.get("SF_CICD_ROLE"),
            "warehouse": settings.get("SF_CICD_WAREHOUSE"),
            "database": settings.get("SF_CICD_DATABASE")
        }
        self.session = Session.builder.configs(self.conn).create()

    