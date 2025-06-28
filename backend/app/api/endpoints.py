"""
API endpoints for the medical bot application.
"""
import time
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from loguru import logger

from ..models.schemas import (
    QueryRequest,
    QueryResponse,
    HealthCheckResponse,
    ErrorResponse,
    DocumentUploadResponse,
    SourceDocument
)
from ..services import qa_service, vector_store_service, document_processor_service
from ..core.config import settings

# Create API router
router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Ask a medical question",
    description="Submit a medical query and get an AI-generated answer with source documents."
)
async def query_medical_bot(request: QueryRequest) -> QueryResponse:
    """
    Process a medical query and return an AI-generated answer.
    
    Args:
        request: Query request containing the medical question
        
    Returns:
        Response with answer and optional source documents
        
    Raises:
        HTTPException: If query processing fails
    """
    try:
        logger.info(f"Received query: {request.query[:100]}...")
        
        # Process the query using QA service
        response = await qa_service.answer_query(request)
        
        logger.info(f"Query processed successfully in {response.processing_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )


@router.get(
    "/search",
    response_model=List[SourceDocument],
    summary="Search for similar documents",
    description="Find documents similar to a query without generating an answer."
)
async def search_documents(
    query: str,
    limit: int = 4
) -> List[SourceDocument]:
    """
    Search for documents similar to a query.
    
    Args:
        query: Search query
        limit: Maximum number of documents to return (1-10)
        
    Returns:
        List of similar documents
        
    Raises:
        HTTPException: If search fails
    """
    try:
        # Validate limit
        if not 1 <= limit <= 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 10"
            )
        
        logger.info(f"Searching for documents similar to: {query[:100]}...")
        
        # Search for similar documents
        documents = await qa_service.get_similar_documents(query, k=limit)
        
        logger.info(f"Found {len(documents)} similar documents")
        return documents
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document search failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search documents: {str(e)}"
        )


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    summary="Upload a document",
    description="Upload a document file to be processed and added to the knowledge base."
)
async def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
    """
    Upload and process a document file.
    
    Args:
        file: Document file to upload (PDF or TXT)
        
    Returns:
        Upload response with processing details
        
    Raises:
        HTTPException: If upload or processing fails
    """
    try:
        start_time = time.time()
        
        # Validate file type
        allowed_types = ["application/pdf", "text/plain", "text/markdown"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file.content_type}. Allowed: {allowed_types}"
            )
        
        logger.info(f"Processing uploaded file: {file.filename}")
        
        # Read file content
        content = await file.read()
        
        # Process based on file type
        if file.content_type == "application/pdf":
            # For PDF files, we'd need to save temporarily and use PyPDFLoader
            # This is a simplified implementation
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="PDF upload not yet implemented. Please use text files."
            )
        else:
            # Process text content
            text_content = content.decode("utf-8")
            metadata = {
                "filename": file.filename,
                "content_type": file.content_type,
                "upload_time": datetime.now().isoformat()
            }
            
            # Process text into chunks
            chunks = await document_processor_service.process_text(text_content, metadata)
            
            # Add to vector store
            result = await vector_store_service.add_documents(chunks)
            
            processing_time = time.time() - start_time
            
            response = DocumentUploadResponse(
                message="Document uploaded and processed successfully",
                document_id=result["document_ids"][0] if result["document_ids"] else "unknown",
                chunks_created=len(chunks),
                processing_time=processing_time
            )
            
            logger.info(f"Document processed successfully in {processing_time:.2f}s")
            return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}"
        )


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health check",
    description="Check the health status of the medical bot API and its dependencies."
)
async def health_check() -> HealthCheckResponse:
    """
    Perform a health check of the API and its services.
    
    Returns:
        Health check response with service statuses
    """
    try:
        logger.debug("Performing health check...")
        
        # Check individual services
        vector_store_status = await vector_store_service.health_check()
        qa_service_status = await qa_service.health_check()
        
        # Determine overall status
        services = {
            "vector_store": vector_store_status["status"],
            "qa_service": qa_service_status["status"],
            "embeddings": "healthy" if vector_store_status["status"] == "healthy" else "unhealthy"
        }
        
        overall_status = "healthy" if all(
            status == "healthy" for status in services.values()
        ) else "degraded"
        
        response = HealthCheckResponse(
            status=overall_status,
            version=settings.app_version,
            timestamp=datetime.now().isoformat(),
            services=services
        )
        
        logger.debug(f"Health check completed: {overall_status}")
        return response
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )
