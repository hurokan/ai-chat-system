from db.connection import get_conn
from pathlib import Path
import hashlib
import os

BASE_DIR = Path(__file__).parent


ORDERED_DIRS = [
    "migrations",
    "functions",
    "procedures",
    "triggers",
    "seeders"
]


def get_checksum(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def ensure_schema_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            folder TEXT NOT NULL,
            checksum TEXT,
            executed_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(filename, folder)
        )
    """)


def get_applied(cur):
    cur.execute("SELECT filename, folder, checksum FROM schema_migrations")
    return {
        (r[0], r[1]): r[2]
        for r in cur.fetchall()
    }


def mark_done(cur, filename, folder, checksum):
    cur.execute("""
        INSERT INTO schema_migrations (filename, folder, checksum)
        VALUES (%s, %s, %s)
        ON CONFLICT (filename, folder)
        DO UPDATE SET checksum = EXCLUDED.checksum,
                      executed_at = NOW()
    """, (filename, folder, checksum))


def run_sql_file(cur, path):
    with open(path, "r", encoding="utf-8") as f:
        cur.execute(f.read())


def run():
    conn = get_conn()
    cur = conn.cursor()

    ensure_schema_table(cur)
    conn.commit()

    applied = get_applied(cur)

    for folder in ORDERED_DIRS:

        folder_path = BASE_DIR / folder

        if not folder_path.exists():
            continue

        files = sorted(folder_path.glob("*.sql"))

        print(f"\n=== Running {folder.upper()} ===")

        for file in files:

            key = (file.name, folder)
            checksum = get_checksum(file)

            if key in applied and applied[key] == checksum:
                print(f"SKIP: {file.name}")
                continue

            try:
                print(f"RUNNING: {file.name}")

                cur.execute("BEGIN;")

                run_sql_file(cur, file)

                mark_done(cur, file.name, folder, checksum)

                conn.commit()

                print(f"SUCCESS: {file.name}")

            except Exception as e:
                conn.rollback()
                print(f"FAILED: {file.name}")
                print(e)
                break

    cur.close()
    conn.close()


if __name__ == "__main__":
    run()