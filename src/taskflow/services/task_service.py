import os
import psycopg

def create_task(name:str)->dict:
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
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
        "name":row[1],
        "completed":row[2],
    }        


def get_tasks()-> list[dict]:
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, completed
                FROM tasks
                ORDER BY id
                """
            )
            rows=cur.fetchall()
    return [
        {
        "id": row[0],
        "name":row[1],
        "completed":row[2],
        }
        for row in rows
    ]