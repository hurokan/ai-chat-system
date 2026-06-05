import psycopg2

def get_conn():
    return psycopg2.connect(
        host="postgres",
        database="ai_chat",
        user="admin",
        password="admin123"
    )
