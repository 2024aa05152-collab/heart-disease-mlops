"""
Logging configuration for Heart Disease Prediction API
Provides structured logging with both standard and JSON output
"""

import logging
import logging.config
import json
from pathlib import Path
from datetime import datetime
import structlog
from pythonjsonlogger import jsonlogger


# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log file paths
API_LOG_FILE = LOG_DIR / "api.log"
ERROR_LOG_FILE = LOG_DIR / "errors.log"
STRUCTURED_LOG_FILE = LOG_DIR / "structured.json"


def setup_logging():
    """
    Setup comprehensive logging configuration with both text and JSON formatters
    """
    
    # Standard logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "json": {
                "()": jsonlogger.JsonFormatter,
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            },
            "api_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "detailed",
                "filename": str(API_LOG_FILE),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": str(ERROR_LOG_FILE),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            },
            "structured_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "json",
                "filename": str(STRUCTURED_LOG_FILE),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            }
        },
        "loggers": {
            "app": {
                "level": "INFO",
                "handlers": ["console", "api_file", "structured_file"],
                "propagate": False
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console", "api_file"],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["api_file", "structured_file"],
                "propagate": False
            },
            "uvicorn.error": {
                "level": "ERROR",
                "handlers": ["console", "error_file"],
                "propagate": False
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "api_file", "error_file", "structured_file"]
        }
    }
    
    logging.config.dictConfig(logging_config)
    
    # Configure structlog for structured logging
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


def log_request_details(logger: logging.Logger, method: str, path: str, 
                       client_ip: str, headers: dict = None, body: dict = None):
    """
    Log HTTP request details
    
    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        path: Request path
        client_ip: Client IP address
        headers: Request headers
        body: Request body
    """
    logger.info(
        "HTTP Request received",
        extra={
            "method": method,
            "path": path,
            "client_ip": client_ip,
            "headers": str(headers) if headers else None,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


def log_response_details(logger: logging.Logger, status_code: int, 
                        response_time: float, response_size: int = None):
    """
    Log HTTP response details
    
    Args:
        logger: Logger instance
        status_code: HTTP status code
        response_time: Response time in milliseconds
        response_size: Response size in bytes
    """
    logger.info(
        "HTTP Response sent",
        extra={
            "status_code": status_code,
            "response_time_ms": response_time,
            "response_size_bytes": response_size,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


def log_prediction(logger: logging.Logger, input_data: dict, 
                  prediction: int, probability: float, inference_time: float):
    """
    Log prediction details
    
    Args:
        logger: Logger instance
        input_data: Input features
        prediction: Prediction result
        probability: Prediction probability
        inference_time: Inference time in milliseconds
    """
    logger.info(
        "Model prediction completed",
        extra={
            "input_features": str(input_data),
            "prediction": prediction,
            "probability": probability,
            "inference_time_ms": inference_time,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


def log_error(logger: logging.Logger, error_type: str, error_message: str, 
             traceback_info: str = None):
    """
    Log error details
    
    Args:
        logger: Logger instance
        error_type: Type of error
        error_message: Error message
        traceback_info: Traceback information
    """
    logger.error(
        f"Error: {error_type}",
        extra={
            "error_type": error_type,
            "error_message": error_message,
            "traceback": traceback_info,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
