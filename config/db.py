import mysql.connector

from config.constant import DATABASE_DATA


def connect_db():
    """Establish the connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**DATABASE_DATA)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        raise
