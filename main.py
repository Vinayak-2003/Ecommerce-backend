"""
Main entry point for the E-Commerce Backend FastAPI application.
This module initializes the FastAPI app, manages the database session lifecycle,
and includes all relevant API routers.
"""
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from database import models
from config import get_settings
# from database.base import get_ecommercedatabase_db_conn
from database.base import close_db, init_db
from src.address.controller import address_route
from src.auth.controller import auth_router
from src.brand.controller import brand_route
from src.cart.controllers import cart_route
from src.order.controller import order_route
from src.products.controller import product_route
from src.user.controller import user_router
from utilities.logger_middleware import get_logger, log_request, setup_logging

settings = get_settings()


setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """
    Context manager for managing the FastAPI application lifespan.
    Handles database initialization on startup and cleanup on shutdown.
    """
    try:
        logger.info("Initializing database connection pool...")
        await init_db()
    except Exception as e:
        logger.error(f"Error initializing database connection pool: {e}")

    yield

    try:
        logger.info("Closing database connection pool...")
        await close_db()
    except Exception as e:
        logger.error(f"Error closing database connection pool: {e}")


app = FastAPI(title="E-Commerece Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_route)
app.include_router(brand_route)
app.include_router(user_router)
app.include_router(address_route)
app.include_router(order_route)
app.include_router(cart_route)
app.include_router(auth_router)


@app.middleware("http")
async def log_req(request: Request, call_next: Callable):
    return await log_request(request, call_next)


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint for the API.
    Returns a simple hello world message to verify the API is running.
    """
    logger.info("root API called")
    return {"msg": "Hello World!!"}
