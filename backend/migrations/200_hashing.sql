ALTER TABLE documents
ADD COLUMN file_hash VARCHAR(64);

CREATE UNIQUE INDEX idx_documents_file_hash
ON documents(file_hash);

ALTER TABLE document_chunks
ADD COLUMN content_hash VARCHAR(64);

CREATE INDEX idx_chunk_hash
ON document_chunks(content_hash);