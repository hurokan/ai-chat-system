CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id UUID REFERENCES documents(document_id),
    chunk_index INT,
    content TEXT,
    embedding VECTOR(768)
);
