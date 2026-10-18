"""Endpoints de monitorización y comprobación de estado de la API."""

from fastapi import APIRouter
import os
import psycopg

# APIRouter permite agrupar endpoints en un módulo independiente.
# La aplicación principal incorpora estas rutas mediante include_router().
router = APIRouter()


@router.get("/")
def read_root():
    """Comprobación básica de que la API está en funcionamiento."""
    return {"message": "Running"}


@router.get("/health")
def health_check():
    """Comprobación del estado de salud de la aplicación."""
    return {"status": "healthy"}


@router.get("/db-check")
def check_db():
    """Verifica la conectividad con la base de datos PostgreSQL.

    Ejecuta una consulta trivial (``SELECT 1``) para confirmar que la
    conexión está activa. Si la conexión falla, psycopg lanzará
    una excepción que FastAPI devolverá como error 500.
    """
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        result = conn.execute("SELECT 1").fetchone()

        if result is not None:
            return {"db_status": "connected"}

        return {"db_status": "not connected"}