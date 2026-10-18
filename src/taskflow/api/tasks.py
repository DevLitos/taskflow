"""Endpoints CRUD para la gestión de tareas."""

from fastapi import APIRouter, HTTPException, Body, status, Response
from taskflow.schemas.task import TaskCreate, Task
from taskflow.services.task_service import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
)

router = APIRouter()


@router.post("/tasks", response_model=Task, status_code=201)
def add_task(task: TaskCreate):
    """Crea una nueva tarea con el nombre proporcionado."""
    return create_task(task.name)


@router.get("/tasks", response_model=list[Task])
def list_tasks():
    """Devuelve todas las tareas existentes ordenadas por identificador."""
    return get_tasks()


@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    """Obtiene una tarea concreta por su identificador.

    Devuelve 404 si no existe ninguna tarea con el ID proporcionado.
    """
    task = get_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")

    return task


@router.patch("/tasks/{task_id}", response_model=Task)
def edit_task(task_id: int, completed: bool = Body()):
    """Actualiza el estado de completada de una tarea.

    Recibe el nuevo valor booleano directamente en el cuerpo de la petición.
    Devuelve 404 si no existe ninguna tarea con el ID proporcionado.
    """
    updated_task = update_task(task_id, completed)

    if updated_task is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")

    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int):
    """Elimina una tarea por su identificador.

    Devuelve 204 sin contenido si la eliminación fue exitosa,
    o 404 si no existe ninguna tarea con el ID proporcionado.
    """
    deleted = delete_task(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="NOT FOUND")

    return Response(status_code=status.HTTP_204_NO_CONTENT)