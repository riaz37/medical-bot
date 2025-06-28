"""
Question-answering service using LangChain and Google Generative AI.
"""
import time
from typing import Dict, Any, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.schema import Document
from loguru import logger

from ..core.config import settings
from ..models.schemas import QueryRequest, QueryResponse, SourceDocument
from .vector_store import vector_store_service


class QAService:
    """Service for handling question-answering operations."""
    
    def __init__(self):
        """Initialize the QA service."""
        self._llm: Optional[ChatGoogleGenerativeAI] = None
        self._qa_chain: Optional[RetrievalQA] = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the QA service with LLM and retrieval chain."""
        try:
            logger.info("Initializing QA service...")
            
            # Ensure vector store is initialized
            if not vector_store_service._initialized:
                await vector_store_service.initialize()
            
            # Initialize LLM
            self._llm = ChatGoogleGenerativeAI(
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                convert_system_message_to_human=True
            )
            
            # Get retriever from vector store
            retriever = vector_store_service.get_retriever(
                search_kwargs={"k": 4}
            )
            
            # Create QA chain
            self._qa_chain = RetrievalQA.from_chain_type(
                llm=self._llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                verbose=settings.debug
            )
            
            self._initialized = True
            logger.info("QA service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize QA service: {e}")
            raise
    
    def _ensure_initialized(self) -> None:
        """Ensure the service is initialized."""
        if not self._initialized:
            raise RuntimeError("QA service not initialized. Call initialize() first.")
    
    async def answer_query(self, request: QueryRequest) -> QueryResponse:
        """
        Answer a medical query using the QA chain.
        
        Args:
            request: Query request containing the question and options
            
        Returns:
            Query response with answer and sources
        """
        self._ensure_initialized()
        
        start_time = time.time()
        
        try:
            logger.info(f"Processing query: {request.query[:100]}...")
            
            # Invoke the QA chain
            result = await self._qa_chain.ainvoke({"query": request.query})
            
            # Extract answer and source documents
            answer = result["result"]
            source_docs = result.get("source_documents", [])
            
            # Process source documents if requested
            sources = None
            if request.include_sources and source_docs:
                sources = self._process_source_documents(
                    source_docs, 
                    max_sources=request.max_sources
                )
            
            processing_time = time.time() - start_time
            
            response = QueryResponse(
                answer=answer,
                sources=sources,
                query=request.query,
                processing_time=processing_time,
                model_used=settings.llm_model
            )
            
            logger.info(f"Query processed successfully in {processing_time:.2f}s")
            return response
            
        except Exception as e:
            logger.error(f"Failed to process query: {e}")
            raise
    
    def _process_source_documents(
        self, 
        source_docs: List[Document], 
        max_sources: int
    ) -> List[SourceDocument]:
        """
        Process source documents into response format.
        
        Args:
            source_docs: Raw source documents from retrieval
            max_sources: Maximum number of sources to include
            
        Returns:
            List of processed source documents
        """
        processed_sources = []
        
        for doc in source_docs[:max_sources]:
            # Extract content (limit length for response)
            content = doc.page_content
            if len(content) > 500:
                content = content[:500] + "..."
            
            # Create source document
            source = SourceDocument(
                content=content,
                metadata=doc.metadata,
                relevance_score=None  # Could be added if using similarity search with scores
            )
            
            processed_sources.append(source)
        
        return processed_sources
    
    async def get_similar_documents(
        self, 
        query: str, 
        k: int = 4
    ) -> List[SourceDocument]:
        """
        Get similar documents for a query without generating an answer.
        
        Args:
            query: Search query
            k: Number of documents to return
            
        Returns:
            List of similar documents
        """
        self._ensure_initialized()
        
        try:
            logger.debug(f"Finding similar documents for: {query[:100]}...")
            
            # Use vector store directly for similarity search
            docs = await vector_store_service.similarity_search(query, k=k)
            
            # Process into response format
            sources = self._process_source_documents(docs, max_sources=k)
            
            logger.debug(f"Found {len(sources)} similar documents")
            return sources
            
        except Exception as e:
            logger.error(f"Failed to find similar documents: {e}")
            raise
    
    async def health_check(self) -> Dict[str, str]:
        """
        Check the health of the QA service.
        
        Returns:
            Health status dictionary
        """
        try:
            if not self._initialized:
                return {"status": "not_initialized"}
            
            # Test with a simple query
            test_query = "What is health?"
            start_time = time.time()
            
            # Just test retrieval, not full QA to avoid API costs
            docs = await vector_store_service.similarity_search(test_query, k=1)
            
            response_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "model": settings.llm_model,
                "response_time": f"{response_time:.2f}s",
                "retrieval_working": "yes" if docs else "no"
            }
            
        except Exception as e:
            logger.error(f"QA service health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}


# Global QA service instance
qa_service = QAService()
