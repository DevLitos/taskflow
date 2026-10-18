"""Punto de entrada de la aplicación FastAPI.

Configura el ciclo de vida (lifespan) y registra los routers de la API.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from taskflow.api.health import router as health_router
from taskflow.api.tasks import router as tasks_router
from taskflow.db.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el arranque y cierre de la aplicación.

    Al iniciar, crea las tablas necesarias en la base de datos
    si no existen. El bloque tras ``yield`` se ejecutaría al apagar
    la aplicación (actualmente no requiere limpieza).
    """
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Registrar los routers que agrupan los endpoints por dominio.
app.include_router(health_router)
app.include_router(tasks_router)
