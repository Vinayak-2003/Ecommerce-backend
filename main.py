from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
import uvicorn
from database.base import get_ecommercedatabase_db_conn
from database.base import Base
from contextlib import asynccontextmanager
from utilities.logger_middleware import log_request, setup_logging, get_logger

from src.products.controller import product_route
from src.user_auth.controller import user_router
from src.brand.controller import brand_route
from src.address.controller import address_route

import database.models

setup_logging()
logger = get_logger(__name__)

# for early project setup - creation of tables, super quick
# @asynccontextmanager
# async def base_lifespan(app: FastAPI):
#     engine = get_ecommercedatabase_db_conn()
#     Base.metadata.create_all(bind=engine)
#     yield

# app = FastAPI(lifespan=base_lifespan)

app = FastAPI(title="E-Commerece Backend")

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

@app.middleware("http")
async def log_req(request: Request, call_next: Callable):
    return await log_request(request, call_next)

@app.get("/", tags=["Root"])
def root():
    logger.info("root API called")
    return {"msg": "Hello World!!"}
