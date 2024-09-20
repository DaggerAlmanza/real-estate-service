import pytest
from config.property_service import (
    fetch_properties_with_filters,
    build_property_query
)


@pytest.fixture(scope="function")
def db_connection(mocker):
    mock_conn = mocker.patch(
        "mysql.connector.connect",
        return_value=mocker.MagicMock()
    )
    conn = mock_conn()
    yield conn
    conn.close()


def test_fetch_properties_with_filters_no_filters(mocker, db_connection):
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
    result = fetch_properties_with_filters(filters)
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


def test_fetch_properties_with_filters_with_filters(mocker, db_connection):
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
    result = fetch_properties_with_filters(filters)
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


def test_build_property_query_no_filters():
    filters = {}
    expected_query = """
        SELECT p.id, p.address, p.city, s.name AS status,
            p.price, p.description, p.year
        FROM property p
        JOIN status_history sh ON p.id = sh.property_id
        JOIN status s ON sh.status_id = s.id
        WHERE sh.update_date = (
            SELECT MAX(sh2.update_date)
            FROM status_history sh2
            WHERE sh2.property_id = p.id
        )
        AND s.name IN ('pre_venta', 'en_venta', 'vendido')
        AND p.city IS NOT NULL
        AND p.city <> ''
        AND p.city <> '0';
    """
    query, params = build_property_query(filters)
    expected_query_normalized = ' '.join(expected_query.split())
    query_normalized = ' '.join(query.split())
    assert query_normalized == expected_query_normalized
    assert params == []


def test_build_property_query_with_filters():
    filters = {
        "year": 2019,
        "city": "bogota",
        "state": "pre_venta"
    }
    expected_query = """
        SELECT p.id, p.address, p.city, s.name AS status,
            p.price, p.description, p.year
        FROM property p
        JOIN status_history sh ON p.id = sh.property_id
        JOIN status s ON sh.status_id = s.id
        WHERE sh.update_date = (
            SELECT MAX(sh2.update_date)
            FROM status_history sh2
            WHERE sh2.property_id = p.id
        )
        AND s.name IN ('pre_venta', 'en_venta', 'vendido')
        AND p.city IS NOT NULL
        AND p.city <> ''
        AND p.city <> '0'
        AND p.year = %s
        AND p.city = %s
        AND s.name = %s;
    """
    query, params = build_property_query(filters)
    expected_query_normalized = ' '.join(expected_query.split())
    query_normalized = ' '.join(query.split())
    assert query_normalized == expected_query_normalized
    assert params == [2019, "bogota", "pre_venta"]


def test_build_property_query_partial_filters():
    filters = {
        "city": "medellin"
    }
    expected_query = """
        SELECT p.id, p.address, p.city, s.name AS status,
               p.price, p.description, p.year
        FROM property p
        JOIN status_history sh ON p.id = sh.property_id
        JOIN status s ON sh.status_id = s.id
        WHERE sh.update_date = (
            SELECT MAX(sh2.update_date)
            FROM status_history sh2
            WHERE sh2.property_id = p.id
        )
        AND s.name IN ('pre_venta', 'en_venta', 'vendido')
        AND p.city IS NOT NULL
        AND p.city <> ''
        AND p.city <> '0'
        AND p.city = %s;
    """
    query, params = build_property_query(filters)
    expected_query_normalized = ' '.join(expected_query.split())
    query_normalized = ' '.join(query.split())
    assert query_normalized == expected_query_normalized
    assert params == ["medellin"]
