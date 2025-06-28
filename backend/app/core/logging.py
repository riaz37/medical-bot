"""
Logging configuration for the application.
"""
import sys
from loguru import logger
from .config import settings


def setup_logging():
    """Configure application logging."""
    # Remove default logger
    logger.remove()
    
    # Add console logger with custom format
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        colorize=True,
    )
    
    # Add file logger for production
    if not settings.debug:
        logger.add(
            "logs/app.log",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
        )
    
    return logger
