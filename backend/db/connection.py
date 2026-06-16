import psycopg2
from pgvector.psycopg2 import register_vector

def get_conn():
    conn = psycopg2.connect(
        host="postgres",
        database="ai_chat",
        user="admin",
        password="admin123"
    )

    register_vector(conn)

    return conn