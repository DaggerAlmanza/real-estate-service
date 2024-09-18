import mysql.connector
import pytest
from app.constant import DATABASE_URL
from app.consult import get_filtered_real_estates


@pytest.fixture(scope="module")
def db_connection():
    conn = mysql.connector.connect(DATABASE_URL)
    yield conn
    conn.close()


def test_get_filtered_real_estates_no_filters(mocker, db_connection):
    filters = {}
    mock_conn = mocker.patch("consult.connect_db", return_value=db_connection)
    mock_cursor = mocker.MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (
            "Calle Falsa 123",
            "Bogotá",
            "pre_venta",
            100000,
            "Descripción inmueble 1"
        ),
        (
            "Av. Siempre Viva 456",
            "Medellín",
            "en_venta",
            150000,
            "Descripción inmueble 2"
        )
    ]
    result = get_filtered_real_estates(filters)
    mock_cursor.execute.assert_called_once()
    expected_result = [
        {
            "direccion": "Calle Falsa 123",
            "ciudad": "Bogotá",
            "estado": "pre_venta",
            "precio_venta": 100000,
            "descripcion": "Descripción inmueble 1"
        },
        {
            "direccion": "Av. Siempre Viva 456",
            "ciudad": "Medellín",
            "estado": "en_venta",
            "precio_venta": 150000,
            "descripcion": "Descripción inmueble 2"
        }
    ]
    assert result == expected_result


def test_get_filtered_real_estates_with_filters(mocker, db_connection):
    filters = {
        "city": "Bogotá",
        "state": "pre_venta"
    }
    mock_conn = mocker.patch("consult.connect_db", return_value=db_connection)
    mock_cursor = mocker.MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (
            "Calle Falsa 123",
            "Bogotá",
            "pre_venta",
            100000,
            "Descripción inmueble 1"
        )
    ]
    result = get_filtered_real_estates(filters)
    mock_cursor.execute.assert_called_once()
    expected_result = [
        {
            "direccion": "Calle Falsa 123",
            "ciudad": "Bogotá",
            "estado": "pre_venta",
            "precio_venta": 100000,
            "descripcion": "Descripción inmueble 1"
        }
    ]
    assert result == expected_result
