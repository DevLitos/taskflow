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

def get_task(task_id: int):
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
    return{
        "id": row[0],
        "name": row[1],
        "completed": row[2],    
    }


def update_task(task_id:int, completed:bool):
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET completed = %s
                WHERE id = %s
                RETURNING id, name, completed
                """,
                (completed,task_id),
            )
            row = cur.fetchone()
    if row is None:
        return None
    return{
        "id": row[0],
        "name": row[1],
        "completed": row[2], 
    }


def delete_task(task_id:int):
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
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