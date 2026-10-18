from fastapi import FastAPI
from contextlib import asynccontextmanager
from taskflow.api.health import router as health_router
from taskflow.api.tasks import router as tasks_router
from taskflow.db.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(tasks_router)


# @app.post("/tasks")
# def add_task():
#     with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
#         with conn.cursor() as cur:
#             cur.execute(
#                 "INSERT INTO test "
#             )
