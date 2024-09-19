import mysql.connector
import pytest
from config.constant import DATABASE_DATA


@pytest.fixture(scope="module")
def db_connection():
    conn = mysql.connector.connect(**DATABASE_DATA)
    yield conn
    conn.close()


def test_get_db_connection(db_connection):
    assert db_connection is not None
