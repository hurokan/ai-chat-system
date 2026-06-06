from pathlib import Path
from db.connection import get_conn

MIGRATION_DIR = "migrations"


def get_applied_migrations(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id SERIAL PRIMARY KEY,
            filename TEXT UNIQUE,
            applied_at TIMESTAMP DEFAULT NOW()
        )
    """)

    cur.execute("SELECT filename FROM schema_migrations")
    return {row[0] for row in cur.fetchall()}


def mark_applied(cur, filename):
    cur.execute("""
        INSERT INTO schema_migrations (filename)
        VALUES (%s)
        ON CONFLICT (filename) DO NOTHING
    """, (filename,))


def run_migrations():
    conn = get_conn()
    cur = conn.cursor()

    applied = get_applied_migrations(cur)

    migration_files = sorted(Path(MIGRATION_DIR).glob("*.sql"))

    for file in migration_files:

        if file.name in applied:
            print(f"SKIP: {file.name}")
            continue

        print(f"RUNNING: {file.name}")

        sql = file.read_text()

        try:
            cur.execute(sql)
            mark_applied(cur, file.name)
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
    run_migrations()