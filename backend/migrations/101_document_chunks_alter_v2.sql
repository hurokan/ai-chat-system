-- Add scoring support for reranking
ALTER TABLE document_chunks
ADD COLUMN IF NOT EXISTS score FLOAT DEFAULT 0;

-- Add metadata (page, section, etc.)
ALTER TABLE document_chunks
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

-- Ensure embedding column is correct
ALTER TABLE document_chunks
ALTER COLUMN embedding TYPE vector(768);