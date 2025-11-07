from fastapi import FastAPI, Request
from typing import Callable
from database.base import get_ecommercedatabase_db_conn
from database.base import Base
from src.products.controller import product_route
from src.user_auth.controller import user_router
from src.brand.controller import brand_route
from contextlib import asynccontextmanager

# for early project setup - creation of tables, super quick
# @asynccontextmanager
# async def base_lifespan(app: FastAPI):
#     engine = get_ecommercedatabase_db_conn()
#     Base.metadata.create_all(bind=engine)
#     yield

# app = FastAPI(lifespan=base_lifespan)

app = FastAPI(title="E-Commerece Backend")

app.include_router(product_route)
app.include_router(brand_route)
app.include_router(user_router)

@app.get("/", tags=["Root"])
def root():
    return {"msg": "Hello World!!"}
