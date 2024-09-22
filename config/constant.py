from os import getenv


DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")

DATABASE_DATA = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
    "database": DB_NAME
}

OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Real Estate API",
        "description": "API for querying real estate properties.",
        "version": "1.0.0"
    },
    "servers": [
        {
            "url": "http://localhost:8000"
        }
    ],
    "paths": {
        "/property": {
            "get": {
                "summary": "Get properties with filters",
                "description": "Retrieve real estate properties based on filters like year, city, and state.",
                "parameters": [
                    {
                        "name": "year",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "integer"
                        },
                        "description": "Filter properties by construction year."
                    },
                    {
                        "name": "city",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Filter properties by city."
                    },
                    {
                        "name": "state",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Filter properties by state."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "A list of real estate properties",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": { "type": "integer" },
                                            "address": { "type": "string" },
                                            "city": { "type": "string" },
                                            "state": { "type": "string" },
                                            "year": { "type": "integer" }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid query parameters"
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        }
    }
}