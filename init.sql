-- FlashForge Database Schema
-- Database initialization script for the FlashForge application

-- Create database (uncomment if needed)
-- CREATE DATABASE flashforge;
-- USE flashforge;

CREATE EXTENSION IF NOT EXISTS vector; -- For vector embeddings

-- Users table: Stores user authentication and profile information
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL CHECK (LENGTH(username) >= 3),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP
);

-- Chats table: Stores chat sessions for each user
CREATE TABLE chats (
    chat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    chat_name VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(chat_name)) > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_archived BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Flashcards table: Stores question-answer pairs for each chat
CREATE TABLE flashcards (
    flashcard_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID NOT NULL,
    question TEXT NOT NULL CHECK (LENGTH(TRIM(question)) > 0),
    answer TEXT NOT NULL CHECK (LENGTH(TRIM(answer)) > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
);

-- Knowledge base table: Stores chunked PDF data with embeddings for RAG system
CREATE TABLE knowledge_base (
    chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID NOT NULL,
    content TEXT NOT NULL CHECK (LENGTH(TRIM(content)) > 0),
    embedding VECTOR(768) NOT NULL,
    source_file_name VARCHAR(255),
    chunk_index INTEGER CHECK (chunk_index >= 0),
    page_number INTEGER CHECK (page_number > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}',
    FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
);

-- Files table: Track uploaded PDF files
CREATE TABLE uploaded_files (
    file_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID NOT NULL,
    original_filename VARCHAR(255) NOT NULL CHECK (LENGTH(TRIM(original_filename)) > 0),
    file_size BIGINT CHECK (file_size > 0 AND file_size <= 104857600), -- Max 100MB
    file_type VARCHAR(50) CHECK (file_type IN ('application/pdf', 'text/plain')),
    upload_path VARCHAR(500),
    processing_status VARCHAR(50) DEFAULT 'pending' CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_last_login ON users(last_login);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_chats_user_id ON chats(user_id);
CREATE INDEX idx_chats_created_at ON chats(created_at);
CREATE INDEX idx_chats_archived ON chats(is_archived);
CREATE INDEX idx_flashcards_chat_id ON flashcards(chat_id);
CREATE INDEX idx_flashcards_active ON flashcards(is_active);
CREATE INDEX idx_knowledge_base_chat_id ON knowledge_base(chat_id);
CREATE INDEX idx_knowledge_base_source_file ON knowledge_base(source_file_name);
CREATE INDEX idx_uploaded_files_chat_id ON uploaded_files(chat_id);
CREATE INDEX idx_uploaded_files_status ON uploaded_files(processing_status);

-- Vector similarity index for knowledge base embeddings (using pgvector)
CREATE INDEX ON knowledge_base USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at columns
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chats_updated_at BEFORE UPDATE ON chats 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_flashcards_updated_at BEFORE UPDATE ON flashcards 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE users IS 'Stores user authentication and profile information for local application';
COMMENT ON TABLE chats IS 'Stores chat sessions where flashcards are generated';
COMMENT ON TABLE flashcards IS 'Stores question-answer pairs generated from chat conversations';
COMMENT ON TABLE knowledge_base IS 'Stores chunked document content with embeddings for RAG system';
COMMENT ON TABLE uploaded_files IS 'Tracks PDF/text files uploaded by users';

COMMENT ON COLUMN knowledge_base.embedding IS 'Vector embedding of the content chunk for similarity search';
COMMENT ON COLUMN knowledge_base.metadata IS 'Additional metadata about the chunk (e.g., topics, keywords)';
COMMENT ON COLUMN uploaded_files.processing_status IS 'Status of file processing: pending, processing, completed, failed';
