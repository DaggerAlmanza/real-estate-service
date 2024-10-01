import pytest

from io import BytesIO
from unittest.mock import Mock

from consult import RealEstateHandler


CITY = "New York"


class TestRealEstateHandler:

    @pytest.fixture
    def handler(self):
        """
        Fixture to create an instance of RealEstateHandler
        with the necessary mocks.
        """
        handler = RealEstateHandler.__new__(RealEstateHandler)
        handler.wfile = BytesIO()
        handler.rfile = BytesIO()
        handler.request = Mock()
        handler.client_address = ("127.0.0.1", 8000)
        handler.server = Mock()
        return handler

    def test_valid_query_parameters(self, handler):
        assert handler.valid_query_parameters(
            {"year": "2022", "city": CITY}
        )
        assert not handler.valid_query_parameters(
            {"year": "2022", "invalid": "param"}
        )

    def test_contains_sql_injection(self, handler):
        assert handler.contains_sql_injection(
            {"city": "New York'; DROP TABLE users;"}
        )
        assert not handler.contains_sql_injection({"city": CITY})

    def test_get_query_parameters(self, handler):
        query = "year=2022&city=New%20York"
        result = handler.get_query_parameters(query)
        assert result == {"year": ["2022"], "city": [CITY]}

    def test_valid_year(self, handler):
        assert handler.valid_year("2022")
        assert not handler.valid_year("invalid")
        assert handler.valid_year(None)

    def test_extract_filters(self, handler):
        query_params = {"year": ["2022"], "city": [CITY]}
        result = handler.extract_filters(query_params)
        assert result == {"year": "2022", "city": CITY, "state": None}
