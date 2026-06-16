from db.connection import get_conn
from services.embedding_service import get_embedding

def main():

    query = "resignation reason CNS"

    vec = get_embedding(query)

    print("Embedding dim:", len(vec))

    conn = get_conn()
    cur = conn.cursor()

    # 🔥 FORCE VECTOR STRING CAST
    vec_str = "[" + ",".join(map(str, vec)) + "]"

    cur.execute("""
        SELECT content
        FROM document_chunks
        ORDER BY embedding <-> %s::vector
        LIMIT 5
    """, (vec_str,))

    rows = cur.fetchall()

    for r in rows:
        print(r[0][:300], "\n")


if __name__ == "__main__":
    main()