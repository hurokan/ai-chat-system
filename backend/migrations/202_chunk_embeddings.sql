CREATE TABLE chunk_embeddings (
    embedding_id UUID PRIMARY KEY,
    chunk_id BIGINT NOT NULL,
    model_id INTEGER NOT NULL,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT NOW()
);