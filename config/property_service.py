from config.db import connect_db


def fetch_properties_with_filters(filters) -> list:
    """Retrieve properties from the database based on filters."""
    conn = connect_db()
    cursor = conn.cursor()
    query, params = build_property_query(filters)
    cursor.execute(query, params)
    result = cursor.fetchall()
    properties = [{
        "direccion": row[1],
        "ciudad": row[2],
        "estado": row[3],
        "precio_venta": int(row[4]),
        "descripcion": row[5]
    } for row in result]
    cursor.close()
    conn.close()
    return properties


def build_property_query(filters):
    """Construct the SQL query for filtering properties."""
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
    """.strip()
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
    return query, params
