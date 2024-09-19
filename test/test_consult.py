import pytest
from consult import get_filtered_real_estates


@pytest.fixture(scope="function")
def db_connection(mocker):
    mock_conn = mocker.patch(
        "mysql.connector.connect",
        return_value=mocker.MagicMock()
    )
    conn = mock_conn()
    yield conn
    conn.close()


def test_get_filtered_real_estates_no_filters(mocker, db_connection):
    filters = {}
    mock_cursor = mocker.MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (
            1,
            "Calle Falsa 123",
            "bogota",
            "pre_venta",
            100000,
            "Descripción inmueble 1",
            2019
        ),
        (
            2,
            "Av. Siempre Viva 456",
            "medellin",
            "en_venta",
            150000,
            "Descripción inmueble 2",
            2020
        )
    ]
    result = get_filtered_real_estates(filters)
    mock_cursor.execute.assert_called_once()
    expected_result = [
        {
            "direccion": "Calle Falsa 123",
            "ciudad": "bogota",
            "estado": "pre_venta",
            "precio_venta": 100000,
            "descripcion": "Descripción inmueble 1"
        },
        {
            "direccion": "Av. Siempre Viva 456",
            "ciudad": "medellin",
            "estado": "en_venta",
            "precio_venta": 150000,
            "descripcion": "Descripción inmueble 2"
        }
    ]
    assert result == expected_result


def test_get_filtered_real_estates_with_filters(mocker, db_connection):
    filters = {
        "city": "bogota",
        "state": "pre_venta",
        "year": 2019
    }
    mock_cursor = mocker.MagicMock()
    db_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (
            1,
            "Calle Falsa 123",
            "bogota",
            "pre_venta",
            100000,
            "Descripción inmueble 1",
            2019
        )
    ]
    result = get_filtered_real_estates(filters)
    mock_cursor.execute.assert_called_once()
    expected_result = [
        {
            "direccion": "Calle Falsa 123",
            "ciudad": "bogota",
            "estado": "pre_venta",
            "precio_venta": 100000,
            "descripcion": "Descripción inmueble 1"
        }
    ]
    assert result == expected_result