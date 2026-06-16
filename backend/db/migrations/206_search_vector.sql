ALTER TABLE document_chunks
ADD COLUMN IF NOT EXISTS search_vector tsvector;

CREATE INDEX IF NOT EXISTS idx_document_chunks_search
ON document_chunks
USING GIN(search_vector);