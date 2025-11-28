import sqlite3
from pathlib import Path

DB_PATH = Path("storage/database.db")
SCHEMA_PATH = Path("storage/schema.sql")


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self._apply_schema()

    def _apply_schema(self):
        """Loads schema.sql and applies it idempotently."""
        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        # SQLite executes multiple statements safely
        self.conn.executescript(schema_sql)
        self.conn.commit()

    # -----------------------
    # Basic query helpers
    # -----------------------

    def query(self, sql, params=None):
        """Return list of rows as dict-like objects."""
        params = params or ()
        cursor = self.conn.execute(sql, params)
        return cursor.fetchall()

    def query_one(self, sql, params=None):
        """Return a single row or None."""
        params = params or ()
        cursor = self.conn.execute(sql, params)
        return cursor.fetchone()

    def execute(self, sql, params=None):
        """Execute a statement (INSERT/UPDATE/DELETE)."""
        params = params or ()
        cursor = self.conn.execute(sql, params)
        self.conn.commit()
        return cursor.rowcount

    def executemany(self, sql, seq_of_params):
        """Execute many INSERT/UPDATE operations."""
        cursor = self.conn.executemany(sql, seq_of_params)
        self.conn.commit()
        return cursor.rowcount

    def insert_and_get_id(self, sql, params=None):
        """Insert a row and return last inserted ID."""
        params = params or ()
        cursor = self.conn.execute(sql, params)
        self.conn.commit()
        return cursor.lastrowid

    # -----------------------
    # Utility
    # -----------------------

    def close(self):
        if self.conn:
            self.conn.close()


# Singleton instance getter
def get_db():
    return Database()