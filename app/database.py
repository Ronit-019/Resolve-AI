import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "resolve.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                customer TEXT NOT NULL,
                email TEXT,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                address TEXT NOT NULL
            )
        """)

        # Add email column to existing databases
        columns = [
            row[1] for row in conn.execute(
                "PRAGMA table_info(orders)"
            ).fetchall()
        ]

        if "email" not in columns:
            conn.execute("ALTER TABLE orders ADD COLUMN email TEXT")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS refunds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        """)


if __name__ == "__main__":
    initialize_database()
    print("Resolve database initialized successfully.")