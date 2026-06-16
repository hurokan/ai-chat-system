CREATE TABLE IF NOT EXISTS document_chunks
(
    id BIGSERIAL PRIMARY KEY,

    document_id UUID NOT NULL,

    filename TEXT,

    chunk_index INTEGER NOT NULL,

    content TEXT NOT NULL,

    embedding VECTOR(768),

    metadata JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_document_chunks_document
ON document_chunks(document_id);