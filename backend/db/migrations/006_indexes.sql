CREATE INDEX IF NOT EXISTS idx_chat_session
ON chat_messages(session_id);

CREATE INDEX IF NOT EXISTS idx_chat_role
ON chat_messages(role);

CREATE INDEX IF NOT EXISTS idx_documents_created
ON document_chunks(created_at);