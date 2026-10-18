import os 
import psycopg

def create_tables():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id serial PRIMARY KEY,
                    name TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT FALSE)
                """)
        conn.commit()