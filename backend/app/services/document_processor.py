"""
Document processing service for loading and splitting documents.
"""
import os
import uuid
from typing import List, Dict, Any, Optional
from pathlib import Path
from langchain.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from loguru import logger

from ..core.config import settings


class DocumentProcessorService:
    """Service for processing and splitting documents."""
    
    def __init__(self):
        """Initialize the document processor service."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    async def load_directory(self, directory_path: str) -> List[Document]:
        """
        Load all documents from a directory.
        
        Args:
            directory_path: Path to the directory containing documents
            
        Returns:
            List of loaded documents
        """
        try:
            logger.info(f"Loading documents from directory: {directory_path}")
            
            if not os.path.exists(directory_path):
                raise FileNotFoundError(f"Directory not found: {directory_path}")
            
            # Load text files
            text_loader = DirectoryLoader(
                directory_path, 
                glob="*.txt",
                loader_cls=TextLoader,
                show_progress=True
            )
            text_docs = text_loader.load()
            
            # Load PDF files
            pdf_loader = DirectoryLoader(
                directory_path,
                glob="*.pdf", 
                loader_cls=PyPDFLoader,
                show_progress=True
            )
            pdf_docs = pdf_loader.load()
            
            all_docs = text_docs + pdf_docs
            logger.info(f"Loaded {len(all_docs)} documents from directory")
            
            return all_docs
            
        except Exception as e:
            logger.error(f"Failed to load documents from directory: {e}")
            raise
    
    async def load_file(self, file_path: str) -> List[Document]:
        """
        Load a single document file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List containing the loaded document
        """
        try:
            logger.info(f"Loading document: {file_path}")
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension in ['.txt', '.md']:
                loader = TextLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            docs = loader.load()
            logger.info(f"Loaded document with {len(docs)} pages/sections")
            
            return docs
            
        except Exception as e:
            logger.error(f"Failed to load document: {e}")
            raise
    
    async def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of document chunks
        """
        try:
            logger.info(f"Splitting {len(documents)} documents into chunks...")
            
            chunks = self.text_splitter.split_documents(documents)
            
            # Add unique IDs to chunks
            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_id"] = str(uuid.uuid4())
                chunk.metadata["chunk_index"] = i
            
            logger.info(f"Created {len(chunks)} document chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to split documents: {e}")
            raise
    
    async def process_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Process raw text into document chunks.
        
        Args:
            text: Raw text to process
            metadata: Optional metadata for the document
            
        Returns:
            List of document chunks
        """
        try:
            logger.info("Processing raw text into chunks...")
            
            # Create document from text
            doc = Document(
                page_content=text,
                metadata=metadata or {}
            )
            
            # Split into chunks
            chunks = await self.split_documents([doc])
            
            logger.info(f"Processed text into {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to process text: {e}")
            raise
    
    async def process_directory(self, directory_path: str) -> Dict[str, Any]:
        """
        Complete processing pipeline for a directory of documents.
        
        Args:
            directory_path: Path to the directory containing documents
            
        Returns:
            Processing results dictionary
        """
        try:
            logger.info(f"Starting complete processing pipeline for: {directory_path}")
            
            # Load documents
            documents = await self.load_directory(directory_path)
            
            if not documents:
                return {
                    "status": "no_documents",
                    "message": "No documents found in directory",
                    "documents_loaded": 0,
                    "chunks_created": 0
                }
            
            # Split documents
            chunks = await self.split_documents(documents)
            
            # Limit chunks if necessary
            if len(chunks) > settings.max_documents:
                logger.warning(f"Limiting chunks to {settings.max_documents} (found {len(chunks)})")
                chunks = chunks[:settings.max_documents]
            
            return {
                "status": "success",
                "documents_loaded": len(documents),
                "chunks_created": len(chunks),
                "chunks": chunks
            }
            
        except Exception as e:
            logger.error(f"Document processing pipeline failed: {e}")
            raise


# Global document processor service instance
document_processor_service = DocumentProcessorService()
