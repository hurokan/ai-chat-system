CREATE TABLE IF NOT EXISTS chat_messages
(
    id BIGSERIAL PRIMARY KEY,

    session_id UUID NOT NULL,

    role VARCHAR(20) NOT NULL,

    message TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT NOW()
);