CREATE TABLE IF NOT EXISTS chat_sessions
(
    id BIGSERIAL PRIMARY KEY,

    session_id UUID UNIQUE NOT NULL,

    document_id UUID,

    created_at TIMESTAMP DEFAULT NOW()
);