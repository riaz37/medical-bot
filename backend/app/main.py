"""
Main FastAPI application for the Medical Bot API.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from .core import settings, setup_logging
from .api import router
from .services import vector_store_service, qa_service, document_processor_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting Medical Bot API...")
    
    try:
        # Initialize services
        await vector_store_service.initialize()
        await qa_service.initialize()
        
        # Process initial documents if needed
        try:
            if settings.skip_document_processing:
                logger.info("Skipping document processing (skip_document_processing=True)")
            else:
                # Check if index already has data
                index_stats = await vector_store_service.get_index_stats()
                if index_stats and index_stats.get('total_vector_count', 0) > 0:
                    logger.info(f"Index already contains {index_stats['total_vector_count']} vectors, skipping document processing")
                else:
                    logger.info("Index is empty, processing documents...")
                    result = await document_processor_service.process_directory("../data")
                    if result["status"] == "success":
                        await vector_store_service.add_documents(result["chunks"])
                        logger.info(f"Processed {result['documents_loaded']} documents into {result['chunks_created']} chunks")
                    else:
                        logger.info("No documents found in ../data directory")
        except Exception as e:
            logger.warning(f"Could not process initial documents: {e}")
        
        logger.info("Medical Bot API started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Medical Bot API...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    # Setup logging
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered medical question answering system using RAG",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_allowed_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(
        router,
        prefix="/api/v1",
        tags=["Medical Bot API"]
    )
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler for unhandled errors."""
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "details": str(exc) if settings.debug else None
            }
        )
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "running",
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    
    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
