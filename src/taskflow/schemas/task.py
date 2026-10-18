from pydantic import BaseModel, Field

# TaskCreate: define qué datos puede enviar el cliente para crear una tarea. 
# No necesita id porque lo genera PostgreSQL, ni completed porque la base de datos establece False por defecto
class TaskCreate(BaseModel):
    name:str = Field(min_length=1, max_length=200)

# Task: define qué datos devolveremos al cliente una vez creada la tarea.
class Task(BaseModel):
    id: int
    name:str = ""
    completed: bool

