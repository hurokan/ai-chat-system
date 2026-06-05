CREATE TABLE IF NOT EXISTS chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID,
    role TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
