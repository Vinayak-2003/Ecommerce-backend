"""
Logging middleware and configuration for the E-Commerce Backend.
Provides request logging, rotating file handlers, and a centralized logger factory.
"""
import json
import logging
import os
import time
from logging.handlers import RotatingFileHandler
from typing import Callable

from fastapi import Request

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

LOG_FILE_PATH = "logs/app.log"


async def log_request(request: Request, call_next: Callable):
    """
    Middleware function that logs every incoming HTTP request and its processing duration.
    """
    logger = logging.getLogger(__name__)
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        duration = time.time() - start_time
        err_log_msg = {
            "event": "Request Failed",
            "url": str(request.url),
            "method": request.method,
            "client_ip": request.client.host,
            "duration": f"{duration: .2f}s",
            "status_code": 500,
            "error_msg": str(e),
        }
        logger.error(json.dumps(err_log_msg))
        raise
    
    duration = time.time() - start_time

    log_msg = {
        "event": "Request Processed",
        "url": str(request.url),
        "method": request.method,
        "client_ip": request.client.host,
        "duration": f"{duration: .2f}s",
        "status_code": response.status_code,
    }

    logger.info(json.dumps({**log_msg}))
    return response


def setup_logging():
    """
    Configures the root logger with a RotatingFileHandler.
    Sets up log formatting and level.
    """
    root_logger = logging.getLogger()
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    root_logger.setLevel(logging.INFO)

    # creating a rotating a file handler of maxbytes 10MB
    handler = RotatingFileHandler(
        LOG_FILE_PATH, mode="a", maxBytes=10 * 1024 * 1024, backupCount=1
    )
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)

    return root_logger


def get_logger(name: str = None):
    return logging.getLogger(name or __name__)
