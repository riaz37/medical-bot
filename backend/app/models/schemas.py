"""
Pydantic models for API request/response schemas.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class QueryRequest(BaseModel):
    """Request model for medical queries."""
    
    query: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="Medical question or query",
        example="What are the symptoms of atrial fibrillation?"
    )
    include_sources: bool = Field(
        default=True,
        description="Whether to include source documents in response"
    )
    max_sources: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of source documents to return"
    )
    
    @validator("query")
    def validate_query(cls, v):
        """Validate and clean the query."""
        return v.strip()


class SourceDocument(BaseModel):
    """Model for source document information."""
    
    content: str = Field(..., description="Document content excerpt")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    relevance_score: Optional[float] = Field(None, description="Relevance score (0-1)")


class QueryResponse(BaseModel):
    """Response model for medical queries."""
    
    answer: str = Field(..., description="AI-generated answer to the query")
    sources: Optional[List[SourceDocument]] = Field(
        None, 
        description="Source documents used for the answer"
    )
    query: str = Field(..., description="Original query")
    processing_time: float = Field(..., description="Processing time in seconds")
    model_used: str = Field(..., description="AI model used for generation")


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    timestamp: str = Field(..., description="Current timestamp")
    services: Dict[str, str] = Field(..., description="Status of dependent services")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")


class DocumentUploadRequest(BaseModel):
    """Request model for document upload."""
    
    filename: str = Field(..., description="Document filename")
    content_type: str = Field(..., description="Document content type")
    
    
class DocumentUploadResponse(BaseModel):
    """Response model for document upload."""
    
    message: str = Field(..., description="Upload status message")
    document_id: str = Field(..., description="Unique document identifier")
    chunks_created: int = Field(..., description="Number of text chunks created")
    processing_time: float = Field(..., description="Processing time in seconds")
