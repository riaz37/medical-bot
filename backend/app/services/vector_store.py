"""
Vector store service for managing document embeddings and retrieval.
"""
import os
from typing import List, Optional, Dict, Any
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from loguru import logger

from ..core.config import settings


class VectorStoreService:
    """Service for managing vector store operations."""
    
    def __init__(self):
        """Initialize the vector store service."""
        self._pinecone_client: Optional[Pinecone] = None
        self._embeddings: Optional[GoogleGenerativeAIEmbeddings] = None
        self._vector_store: Optional[PineconeVectorStore] = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize Pinecone and embeddings."""
        try:
            logger.info("Initializing vector store service...")
            
            # Set up Google API key
            os.environ["GOOGLE_API_KEY"] = settings.google_api_key
            
            # Initialize Pinecone
            self._pinecone_client = Pinecone(api_key=settings.pinecone_api_key)
            
            # Initialize embeddings
            self._embeddings = GoogleGenerativeAIEmbeddings(
                model=settings.embedding_model
            )
            
            # Initialize vector store
            self._vector_store = PineconeVectorStore.from_existing_index(
                index_name=settings.pinecone_index_name,
                embedding=self._embeddings
            )
            
            self._initialized = True
            logger.info("Vector store service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector store service: {e}")
            raise
    
    def _ensure_initialized(self) -> None:
        """Ensure the service is initialized."""
        if not self._initialized:
            raise RuntimeError("Vector store service not initialized. Call initialize() first.")
    
    async def add_documents(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of documents to add
            
        Returns:
            Dictionary with operation results
        """
        self._ensure_initialized()
        
        try:
            logger.info(f"Adding {len(documents)} documents to vector store...")
            
            # Add documents to vector store
            doc_ids = await self._vector_store.aadd_documents(documents)
            
            result = {
                "documents_added": len(documents),
                "document_ids": doc_ids,
                "status": "success"
            }
            
            logger.info(f"Successfully added {len(documents)} documents")
            return result
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    async def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        score_threshold: Optional[float] = None
    ) -> List[Document]:
        """
        Perform similarity search in the vector store.
        
        Args:
            query: Search query
            k: Number of documents to return
            score_threshold: Minimum similarity score threshold
            
        Returns:
            List of relevant documents
        """
        self._ensure_initialized()
        
        try:
            logger.debug(f"Performing similarity search for: {query[:100]}...")
            
            if score_threshold:
                # Use similarity search with score threshold
                docs_with_scores = await self._vector_store.asimilarity_search_with_score(
                    query, k=k
                )
                docs = [
                    doc for doc, score in docs_with_scores 
                    if score >= score_threshold
                ]
            else:
                # Regular similarity search
                docs = await self._vector_store.asimilarity_search(query, k=k)
            
            logger.debug(f"Found {len(docs)} relevant documents")
            return docs
            
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            raise
    
    def get_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Get a retriever instance for the vector store.
        
        Args:
            search_kwargs: Additional search parameters
            
        Returns:
            Retriever instance
        """
        self._ensure_initialized()
        
        search_kwargs = search_kwargs or {"k": 4}
        return self._vector_store.as_retriever(search_kwargs=search_kwargs)
    
    async def get_index_stats(self) -> Optional[Dict[str, Any]]:
        """
        Get statistics about the Pinecone index.

        Returns:
            Index statistics or None if failed
        """
        if not self._initialized or not self._pinecone_client:
            return None

        try:
            index = self._pinecone_client.Index(settings.pinecone_index_name)
            stats = index.describe_index_stats()
            return {
                "total_vector_count": stats.total_vector_count,
                "index_name": settings.pinecone_index_name
            }
        except Exception as e:
            logger.error(f"Failed to get index stats: {e}")
            return None

    async def health_check(self) -> Dict[str, str]:
        """
        Check the health of the vector store service.

        Returns:
            Health status dictionary
        """
        try:
            if not self._initialized:
                return {"status": "not_initialized"}

            # Try a simple operation to check connectivity
            index = self._pinecone_client.Index(settings.pinecone_index_name)
            stats = index.describe_index_stats()

            return {
                "status": "healthy",
                "total_vectors": str(stats.total_vector_count),
                "index_name": settings.pinecone_index_name
            }

        except Exception as e:
            logger.error(f"Vector store health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}


# Global vector store service instance
vector_store_service = VectorStoreService()
