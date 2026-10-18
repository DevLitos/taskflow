from fastapi import APIRouter
from taskflow.schemas.task import TaskCreate, TaskRead
from taskflow.services.task_service import create_task,get_tasks

router = APIRouter()

@router.post("/tasks", response_model=TaskRead, status_code=201)
def add_task(task:TaskCreate):
    return create_task(task.name)

@router.get("/tasks", response_model=list[TaskRead])
def list_tasks():
    return get_tasks()