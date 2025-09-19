from fastapi import FastAPI
from database.base import get_ecommercedatabase_db_conn
from schemas.products_schema import Base
from router.product_router import product_route
from router.brand_router import brand_route
from contextlib import asynccontextmanager

# for early project setup - creation of tables, super quick
# @asynccontextmanager
# async def base_lifespan(app: FastAPI):
#     engine = get_ecommercedatabase_db_conn()
#     Base.metadata.create_all(bind=engine)
#     yield

# app = FastAPI(lifespan=base_lifespan)

app = FastAPI()
app.include_router(product_route)
app.include_router(brand_route)

@app.get("/", tags=["Root"])
def root():
    return {"msg": "Hello World!!"}
