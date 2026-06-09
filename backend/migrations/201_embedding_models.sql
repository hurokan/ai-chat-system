CREATE TABLE embedding_models (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100),
    dimension INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);