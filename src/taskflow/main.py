from fastapi import FastAPI
import os
import psycopg

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/db-check")
def check_db():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        result = conn.execute("SELECT 1").fetchone()
        if result is not None:
            return {"db_status": "connected"}
        else:
            return {"db_status": "not connected"}                                        