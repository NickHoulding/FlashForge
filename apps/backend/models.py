from exceptions import (
    InvalidUsernameException, InvalidChatNameException,
    InvalidFlashcardException, InvalidContentException, InvalidFileException
)
from sqlalchemy import (
    Column, String, Text, Integer, BigInteger, Boolean, DateTime, 
    ForeignKey, CheckConstraint, Index, Enum as SQLEnum, TIMESTAMP
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, validates
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import func
import uuid
import enum

Base = declarative_base()

class ProcessingStatus(enum.Enum):
    """Enum for file processing status"""
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"

class FileType(enum.Enum):
    """Enum for supported file types"""
    PDF = "application/pdf"
    TEXT = "text/plain"


class User(Base):
    """User model for authentication and profile information"""
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    last_login = Column(DateTime(timezone=True), nullable=True, index=True)

    # Relationships
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")

    # Table constraints
    __table_args__ = (
        CheckConstraint("LENGTH(TRIM(username)) > 0", name="check_username_not_empty"),
    )

    @validates('username')
    def validate_username(self, key, username):
        if not username or not username.strip():
            raise InvalidUsernameException("Username cannot be empty", 400)
        return username.strip()

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}')>"


class Chat(Base):
    """Chat model for storing chat sessions"""
    __tablename__ = "chats"

    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    chat_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_archived = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="chats")
    flashcards = relationship("Flashcard", back_populates="chat", cascade="all, delete-orphan")
    knowledge_base_entries = relationship("KnowledgeBase", back_populates="chat", cascade="all, delete-orphan")
    uploaded_files = relationship("UploadedFile", back_populates="chat", cascade="all, delete-orphan")

    # Table constraints
    __table_args__ = (
        CheckConstraint("LENGTH(TRIM(chat_name)) > 0", name="check_chat_name_not_empty"),
    )

    @validates('chat_name')
    def validate_chat_name(self, key, chat_name):
        if not chat_name or not chat_name.strip():
            raise InvalidChatNameException("Chat name cannot be empty", 400)
        return chat_name.strip()

    def __repr__(self):
        return f"<Chat(chat_id={self.chat_id}, chat_name='{self.chat_name}', user_id={self.user_id})>"


class Flashcard(Base):
    """Flashcard model for storing question-answer pairs"""
    __tablename__ = "flashcards"

    flashcard_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.chat_id", ondelete="CASCADE"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    # Relationships
    chat = relationship("Chat", back_populates="flashcards")

    # Table constraints
    __table_args__ = (
        CheckConstraint("LENGTH(TRIM(question)) > 0", name="check_question_not_empty"),
        CheckConstraint("LENGTH(TRIM(answer)) > 0", name="check_answer_not_empty"),
    )

    @validates('question')
    def validate_question(self, key, question):
        if not question or not question.strip():
            raise InvalidFlashcardException("Question cannot be empty", 400)
        return question.strip()

    @validates('answer')
    def validate_answer(self, key, answer):
        if not answer or not answer.strip():
            raise InvalidFlashcardException("Answer cannot be empty", 400)
        return answer.strip()

    def __repr__(self):
        return f"<Flashcard(flashcard_id={self.flashcard_id}, chat_id={self.chat_id})>"


class KnowledgeBase(Base):
    """Knowledge base model for storing chunked document content with embeddings"""
    __tablename__ = "knowledge_base"

    chunk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.chat_id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768), nullable=False)  # 768-dimensional vector for embeddings
    source_file_name = Column(String(255), nullable=True, index=True)
    chunk_index = Column(Integer, nullable=True)
    page_number = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    file_metadata = Column(JSONB, default=dict, nullable=False)

    # Relationships
    chat = relationship("Chat", back_populates="knowledge_base_entries")

    # Table constraints
    __table_args__ = (
        CheckConstraint("LENGTH(TRIM(content)) > 0", name="check_content_not_empty"),
        CheckConstraint("chunk_index >= 0", name="check_chunk_index_non_negative"),
        CheckConstraint("page_number > 0", name="check_page_number_positive"),
        # Vector similarity index will be created via migration
        Index('idx_knowledge_base_embedding_cosine', 'embedding', postgresql_using='ivfflat',
              postgresql_with={'lists': 100}, postgresql_ops={'embedding': 'vector_cosine_ops'}),
    )

    @validates('content')
    def validate_content(self, key, content):
        if not content or not content.strip():
            raise InvalidContentException("Content cannot be empty", 400)
        return content.strip()

    @validates('chunk_index')
    def validate_chunk_index(self, key, chunk_index):
        if chunk_index is not None and chunk_index < 0:
            raise InvalidContentException("Chunk index must be non-negative", 400)
        return chunk_index

    @validates('page_number')
    def validate_page_number(self, key, page_number):
        if page_number is not None and page_number <= 0:
            raise InvalidContentException("Page number must be positive", 400)
        return page_number

    def __repr__(self):
        return f"<KnowledgeBase(chunk_id={self.chunk_id}, chat_id={self.chat_id}, source_file='{self.source_file_name}')>"


class UploadedFile(Base):
    """Uploaded file model for tracking PDF/text files"""
    __tablename__ = "uploaded_files"

    file_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.chat_id", ondelete="CASCADE"), nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    file_size = Column(BigInteger, nullable=True)
    file_type = Column(SQLEnum(FileType), nullable=True)
    upload_path = Column(String(500), nullable=True)
    processing_status = Column(SQLEnum(ProcessingStatus), default=ProcessingStatus.PENDING, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    chat = relationship("Chat", back_populates="uploaded_files")

    # Table constraints
    __table_args__ = (
        CheckConstraint("LENGTH(TRIM(original_filename)) > 0", name="check_filename_not_empty"),
        CheckConstraint("file_size > 0 AND file_size <= 104857600", name="check_file_size_range"),  # Max 100MB
    )

    @validates('original_filename')
    def validate_filename(self, key, filename):
        if not filename or not filename.strip():
            raise InvalidFileException("Filename cannot be empty", 400)
        return filename.strip()

    @validates('file_size')
    def validate_file_size(self, key, file_size):
        if file_size is not None:
            if file_size <= 0:
                raise InvalidFileException("File size must be positive", 400)
            if file_size > 104857600:  # 100MB in bytes
                raise InvalidFileException("File size cannot exceed 100MB", 400)
        return file_size

    def __repr__(self):
        return f"<UploadedFile(file_id={self.file_id}, filename='{self.original_filename}', status={self.processing_status})>"


# Additional indexes to match the SQL schema performance optimizations
# These will be created automatically when the models are used with Alembic migrations

# Note: The vector similarity index for knowledge_base embeddings is defined in the KnowledgeBase model
# The following indexes are already handled by SQLAlchemy through the index=True parameters:
# - idx_users_username, idx_users_last_login, idx_users_active
# - idx_chats_user_id, idx_chats_created_at, idx_chats_archived  
# - idx_flashcards_chat_id, idx_flashcards_active
# - idx_knowledge_base_chat_id, idx_knowledge_base_source_file
# - idx_uploaded_files_chat_id, idx_uploaded_files_status
