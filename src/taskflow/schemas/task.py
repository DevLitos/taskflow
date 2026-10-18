"""Esquemas Pydantic para validación de peticiones y respuestas de tareas.

FastAPI utiliza estos modelos para:
- Validar automáticamente los datos de entrada.
- Serializar las respuestas al formato JSON.
- Generar la documentación interactiva (Swagger / ReDoc).
"""

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Datos requeridos para crear una nueva tarea.

    No incluye ``id`` (lo genera PostgreSQL) ni ``completed``
    (la base de datos lo establece a False por defecto).
    """

    name: str = Field(min_length=1, max_length=200)


class Task(BaseModel):
    """Representación completa de una tarea devuelta al cliente."""

    id: int
    name: str = ""
    completed: bool
