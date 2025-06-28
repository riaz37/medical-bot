"""
Application configuration management with environment variable validation.
"""
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    app_name: str = Field(default="Medical Bot API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # API Keys
    google_api_key: str = Field(..., description="Google AI API key")
    pinecone_api_key: str = Field(..., description="Pinecone API key")
    pinecone_index_name: str = Field(..., description="Pinecone index name")
    
    # CORS settings
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Document processing settings
    chunk_size: int = Field(default=1000, ge=100, le=4000, description="Text chunk size")
    chunk_overlap: int = Field(default=100, ge=0, le=500, description="Text chunk overlap")
    max_documents: int = Field(default=1000, ge=1, description="Maximum documents to process")
    
    # AI model settings
    embedding_model: str = Field(default="models/embedding-001", description="Embedding model name")
    llm_model: str = Field(default="gemini-2.0-flash", description="LLM model name")
    llm_temperature: float = Field(default=0.2, ge=0.0, le=1.0, description="LLM temperature")

    # Processing settings
    skip_document_processing: bool = Field(default=False, description="Skip document processing if index has data")
    
    def get_allowed_origins(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


# Global settings instance
settings = Settings()
