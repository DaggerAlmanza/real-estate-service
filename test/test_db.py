import mysql.connector
import pytest
from app.constant import DATABASE_URL


@pytest.fixture(scope="module")
def db_connection():
    conn = mysql.connector.connect(DATABASE_URL)
    yield conn
    conn.close()


def test_get_db_connection(db_connection):
    assert db_connection is not None
