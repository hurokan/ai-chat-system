ALTER TABLE chat_messages
ADD COLUMN IF NOT EXISTS document_id UUID;