-- 1. Drop FK first (SAFE)
ALTER TABLE document_chunks
DROP CONSTRAINT IF EXISTS document_chunks_document_id_fkey;

ALTER TABLE documents
ALTER COLUMN document_id TYPE UUID
USING document_id::uuid;

ALTER TABLE document_chunks
ALTER COLUMN document_id TYPE UUID
USING document_id::uuid;

ALTER TABLE documents
ADD CONSTRAINT documents_document_id_unique
UNIQUE (document_id);

ALTER TABLE document_chunks
ADD CONSTRAINT document_chunks_document_id_fkey
FOREIGN KEY (document_id)
REFERENCES documents(document_id)
ON DELETE CASCADE;