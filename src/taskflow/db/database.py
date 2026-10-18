"""Inicialización del esquema de la base de datos.

Crea las tablas necesarias al arrancar la aplicación,
utilizando IF NOT EXISTS para ser idempotente.
"""

import os
import psycopg


def create_tables() -> None:
    """Crea la tabla ``tasks`` en PostgreSQL si no existe.

    Se ejecuta durante el lifespan de la aplicación para garantizar
    que el esquema esté listo antes de atender peticiones.
    """
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id serial PRIMARY KEY,
                    name TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT FALSE)
                """)
        conn.commit()