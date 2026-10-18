"""Capa de servicios para la gestión de tareas.

Contiene la lógica de negocio y las consultas SQL que conectan
los endpoints de la API con la base de datos PostgreSQL.
Cada función abre su propia conexión mediante la variable
de entorno DATABASE_URL.
"""

import os
import psycopg


def create_task(name: str) -> dict:
    """Crea una tarea y devuelve sus datos principales.

    Args:
        name: Nombre descriptivo de la tarea.

    Returns:
        Diccionario con id, name y completed de la tarea creada.
    """
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            # RETURNING evita una segunda consulta para obtener los datos insertados.
            cur.execute(
                """
                INSERT INTO tasks (name)
                VALUES (%s)
                RETURNING id, name, completed
                """,
                (name,),
            )
            row = cur.fetchone()

    return {
        "id": row[0],
        "name": row[1],
        "completed": row[2],
    }


def get_tasks() -> list[dict]:
    """Obtiene todas las tareas ordenadas por su identificador.

    Returns:
        Lista de diccionarios, uno por tarea, con id, name y completed.
    """
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, completed
                FROM tasks
                ORDER BY id
                """
            )
            rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1],
            "completed": row[2],
        }
        for row in rows
    ]


def get_task(task_id: int) -> dict | None:
    """Busca una tarea por su identificador.

    Args:
        task_id: Identificador único de la tarea.

    Returns:
        Diccionario con los datos de la tarea, o None si no existe.
    """
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, completed
                FROM tasks
                WHERE id = %s
                """,
                (task_id,),
            )
            row = cur.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "completed": row[2],
    }


def update_task(task_id: int, completed: bool) -> dict | None:
    """Actualiza el estado de una tarea y devuelve la tarea modificada.

    Args:
        task_id: Identificador único de la tarea.
        completed: Nuevo estado de completada.

    Returns:
        Diccionario con los datos actualizados, o None si no existe.
    """
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            # RETURNING devuelve la fila modificada en una sola operación.
            cur.execute(
                """
                UPDATE tasks
                SET completed = %s
                WHERE id = %s
                RETURNING id, name, completed
                """,
                (completed, task_id),
            )
            row = cur.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "completed": row[2],
    }


def delete_task(task_id: int) -> bool:
    """Elimina una tarea y devuelve True si la operación tuvo efecto.

    Args:
        task_id: Identificador único de la tarea a eliminar.

    Returns:
        True si se eliminó la tarea; False si no existía.
    """
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            # RETURNING confirma si la fila existía sin necesitar rowcount.
            cur.execute(
                """
                DELETE FROM tasks
                WHERE id = %s
                RETURNING id
                """,
                (task_id,),
            )
            row = cur.fetchone()

    return row is not None