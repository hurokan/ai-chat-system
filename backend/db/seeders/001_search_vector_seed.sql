UPDATE document_chunks
SET search_vector = to_tsvector('english', content)
WHERE search_vector IS NULL;