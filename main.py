from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
import uvicorn
# from database.base import get_ecommercedatabase_db_conn
from database.base import Base
from contextlib import asynccontextmanager
from utilities.logger_middleware import log_request, setup_logging, get_logger

from src.products.controller import product_route
from src.user_auth.controller import user_router
from src.brand.controller import brand_route
from src.address.controller import address_route
from src.order.controller import order_route
from src.cart.controllers import cart_route

import database.models
from database.base import init_db, close_db

from config import get_settings

settings = get_settings()


setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info(f"Initializing database connection pool...")
        await init_db()
    except Exception as e:
        logger.error(f"Error initializing database connection pool: {e}")

    yield

    try:
        logger.info(f"Closing database connection pool...")
        await close_db()
    except Exception as e:
        logger.error(f"Error closing database connection pool: {e}")

app = FastAPI(title="E-Commerece Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.middleware("http")
async def log_req(request: Request, call_next: Callable):
    return await log_request(request, call_next)

@app.get("/", tags=["Root"])
def root():
    logger.info("root API called")
    return {"msg": "Hello World!!"}
