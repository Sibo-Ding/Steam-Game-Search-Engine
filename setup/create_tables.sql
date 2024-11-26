CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE steam (
    name VARCHAR(250) PRIMARY KEY,
    original_price NUMERIC(10, 2),
    release_date DATE,
    description VARCHAR(500),
    all_reviews_summary VARCHAR(30),
    developer VARCHAR(1000),
    supported_languages VARCHAR(1500),
    tags VARCHAR(500),
    features VARCHAR(500),
    embeddings VECTOR(384)
);