from fastapi import FastAPI
from database.base import get_ecommercebackend_db_conn
from schemas.products_schema import Base
from router.product_router import product_route
from contextlib import asynccontextmanager

# for early project setup - creation of tables, super quick
@asynccontextmanager
async def base_lifespan(app: FastAPI):
    engine = get_ecommercebackend_db_conn()
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=base_lifespan)
app.include_router(product_route)

@app.get("/", tags=["Root"])
def root():
    return {"msg": "Hello World!!"}
