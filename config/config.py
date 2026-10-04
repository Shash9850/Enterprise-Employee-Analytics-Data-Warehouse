import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()


def get_config_value(key, default=None):
    """Return a configuration value from Streamlit Secrets or environment variables."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        # Streamlit Secrets may not exist during local execution.
        pass

    return os.getenv(key, default)


DATABASE_CONFIG = {
    "host": get_config_value("MYSQL_HOST"),
    "port": int(get_config_value("MYSQL_PORT", 3306)),
    "user": get_config_value("MYSQL_USER"),
    "password": get_config_value("MYSQL_PASSWORD"),
    "database": get_config_value("MYSQL_DATABASE")
}


DW_DATABASE_CONFIG = {
    "host": get_config_value("MYSQL_HOST"),
    "port": int(get_config_value("MYSQL_PORT", 3306)),
    "user": get_config_value("MYSQL_USER"),
    "password": get_config_value("MYSQL_PASSWORD"),
    "database": get_config_value("MYSQL_DW_DATABASE")
}