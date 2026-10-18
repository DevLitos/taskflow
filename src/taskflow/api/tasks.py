from fastapi import APIRouter, HTTPException,Body,status,Response
from taskflow.schemas.task import TaskCreate, Task
from taskflow.services.task_service import create_task,get_tasks,get_task, update_task, delete_task

router = APIRouter()

@router.post("/tasks", response_model=Task, status_code=201)
def add_task(task:TaskCreate):
    return create_task(task.name)

@router.get("/tasks", response_model=list[Task])
def list_tasks():
    return get_tasks()

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    task = get_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return task

@router.patch("/tasks/{task_id}", response_model=Task)
def edit_task(task_id:int, completed:bool = Body()):
    updated_task = update_task(task_id, completed)

    if updated_task is None:
            raise HTTPException(status_code=404, detail="NOT FOUND")
    return updated_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id:int):
    deleted = delete_task(task_id)

    if not deleted:
         raise HTTPException(status_code=404, detail="NOT FOUND")
    return Response(status_code=status.HTTP_204_NO_CONTENT)