CREATE EXTENSION IF NOT EXISTS vector;

SELECT * FROM pg_extension WHERE extname = 'vector';

DO $$ 
BEGIN
    RAISE NOTICE 'Database initialized successfully!';
    RAISE NOTICE 'pgvector extension enabled.';
END $$;
