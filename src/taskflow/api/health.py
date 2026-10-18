from fastapi import APIRouter
import os
import psycopg

# APIRouter permite agrupar endpoints en un módulo independiente. 
# Después, la aplicación principal incorpora esas rutas mediante include_router()
router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Running"}

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.get("/db-check")
def check_db():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        result = conn.execute("SELECT 1").fetchone()

        if result is not None:
            return {"db_status": "connected"}

        return {"db_status": "not connected"}