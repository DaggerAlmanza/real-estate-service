import json
from config.db import connect_db
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class RealEstateHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/property":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            query_components = parse_qs(parsed_path.query)
            filters = {
                "year": query_components.get("year", [None])[0],
                "city": query_components.get("city", [None])[0],
                "state": query_components.get("state", [None])[0]
            }
            try:
                real_estates = get_filtered_real_estates(filters)
                response = {
                    "data": real_estates,
                    "message": "These are all the available properties."
                }
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                error_response = {
                    "data": None,
                    "message": "An internal error occurred.",
                    "detail": str(e)
                }
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            error_response = {
                "data": None,
                "message": "Resource not found.",
                "detail": "The requested path or resource does not exist."
            }
            self.wfile.write(json.dumps(error_response).encode())


def get_filtered_real_estates(filters) -> list:
    """
    We perform the query for the latest status, then apply
    the specified filters, and finally format it as desired.
    """
    conn = connect_db()
    cursor = conn.cursor()

    query = """
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
    """

    params = []
    if filters.get("year"):
        query += " AND p.year = %s"
        params.append(filters["year"])
    if filters.get("city"):
        query += " AND p.city = %s"
        params.append(filters["city"])
    if filters.get("state"):
        query += " AND s.name = %s"
        params.append(filters["state"])
    query += ";"

    cursor.execute(query, params)
    result = cursor.fetchall()

    real_estates = [{
        "direccion": row[1],
        "ciudad": row[2],
        "estado": row[3],
        "precio_venta": int(row[4]),
        "descripcion": row[5],
        # "año": int(row[6]) if row[6] else None
    } for row in result]

    cursor.close()
    conn.close()
    return real_estates


if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, RealEstateHandler)
    print("Servicio de consulta de inmuebles corriendo en el puerto 8000...")
    httpd.serve_forever()
