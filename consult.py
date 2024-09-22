import json
import re
from config.property_service import fetch_properties_with_filters
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class RealEstateHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/property":
            query_components = self.get_query_parameters(parsed_path.query)
            filters = self.extract_filters(query_components)
            response = self.validate_query_integrity(
                query_components,
                filters
            )
            if not response:
                return
            try:
                real_estates = fetch_properties_with_filters(filters)
                self.respond_with_success(real_estates)
            except Exception as e:
                self.respond_with_error(500, "Internal server error", str(e))
        elif self.path == "/docs":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("config/docs/index.html", "r") as f:
                html_content = f.read()
                self.wfile.write(html_content.encode())
        elif self.path == "/swagger.yaml":
            self.send_response(200)
            self.send_header("Content-Type", "application/x-yaml")
            self.end_headers()
            with open("config/docs/swagger.yaml", "r") as f:
                html_content = f.read()
                self.wfile.write(html_content.encode())
        else:
            self.respond_with_error(
                404,
                "Resource not found",
                "The requested path or resource does not exist."
            )

    def validate_query_integrity(
        self,
        query_components,
        filters: dict
    ) -> dict:
        """Validate the information received from the query."""
        response = {}
        if not self.valid_query_parameters(query_components):
            self.respond_with_error(
                400,
                "Invalid query parameters",
                "Only 'year', 'city', and 'state' are allowed."
            )
            return response
        if not self.valid_year(filters["year"]):
            self.respond_with_error(
                400,
                "Invalid 'year' parameter",
                "'year' must be a number."
            )
            return response
        if self.contains_sql_injection(filters):
            self.respond_with_error(
                400,
                "Possible SQL injection",
                "Invalid characters in parameters."
            )
            return response
        return filters

    def valid_query_parameters(self, query_params) -> bool:
        """Validate that only allowed parameters are present."""
        allowed_params = {"year", "city", "state"}
        return set(query_params.keys()).issubset(allowed_params)

    def contains_sql_injection(self, filters) -> bool:
        """Check for basic SQL injection patterns in filters."""
        sql_injection_pattern = re.compile(
            r"(?i)\b(SELECT|FROM|AND|OR|WHERE|DROP|TABLE)\b|['\";\-]"
        )
        return any(
            value and sql_injection_pattern.search(value)
            for value in filters.values()
        )

    def get_query_parameters(self, query):
        """Parse query parameters from the URL."""
        return parse_qs(query)

    def valid_year(self, year: int) -> bool:
        """Check if 'year' is a valid number."""
        return year is None or year.isdigit()

    def extract_filters(self, query_params) -> dict:
        """Extract filters from query parameters."""
        return {
            "year": query_params.get("year", [None])[0],
            "city": query_params.get("city", [None])[0],
            "state": query_params.get("state", [None])[0]
        }

    def respond_with_success(self, data):
        """Send a successful response with real estate data."""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {
            "data": data,
            "message": "These are all the available properties."
        }
        self.wfile.write(json.dumps(response).encode())

    def respond_with_error(self, status_code, message, detail):
        """Send an error response."""
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        error_response = {
            "data": None,
            "message": message,
            "detail": detail
        }
        self.wfile.write(json.dumps(error_response).encode())


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, RealEstateHandler)
    print("Real estate query service running on port 8000...")
    httpd.serve_forever()
