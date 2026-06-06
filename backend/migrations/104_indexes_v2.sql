-- vector index (critical for performance)
CREATE INDEX IF NOT EXISTS idx_document_chunks_embedding
ON document_chunks
USING ivfflat (embedding vector_cosine_ops);

-- document filter index
CREATE INDEX IF NOT EXISTS idx_document_chunks_doc_id
ON document_chunks(document_id);

-- session chat performance
CREATE INDEX IF NOT EXISTS idx_chat_messages_session
ON chat_messages(session_id);