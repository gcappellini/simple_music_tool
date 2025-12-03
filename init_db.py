import sqlite3
import os

DB_PATH = "data/personal.db"
SCHEMA_PATH = "schema.sql"

def init_db():
    # Ensure folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Create DB if not exists and apply schema
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())

    print(f"✅ Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()