-- Add metadata support (for future filtering, tagging)
ALTER TABLE documents
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

-- Add document status (processing, ready, failed)
ALTER TABLE documents
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'ready';