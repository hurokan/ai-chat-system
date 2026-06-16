CREATE OR REPLACE FUNCTION update_chunk_search_vector()
RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        to_tsvector('english', COALESCE(NEW.content,''));

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_chunk_search_vector
ON document_chunks;

CREATE TRIGGER trg_chunk_search_vector
BEFORE INSERT OR UPDATE
ON document_chunks
FOR EACH ROW
EXECUTE FUNCTION update_chunk_search_vector();