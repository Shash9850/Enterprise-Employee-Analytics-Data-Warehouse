import mysql.connector
from config.config import DATABASE_CONFIG


class DatabaseConnection:
    """Manage the application's MySQL database connection."""

    _instance = None

    def __new__(cls):
        """Create only one DatabaseConnection instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        """Initialize the database connection."""
        if not hasattr(self, "connection"):
            self.connection = None

    def connect(self):
        """Establish a connection to the MySQL database."""
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=DATABASE_CONFIG["host"],
                port=DATABASE_CONFIG["port"],
                user=DATABASE_CONFIG["user"],
                password=DATABASE_CONFIG["password"],
                database=DATABASE_CONFIG["database"]
            )

        return self.connection

    def close(self):
        """Close the database connection if it is open."""
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            self.connection = None