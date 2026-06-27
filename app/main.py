from contextlib import asynccontextmanager
from app.routes import transform
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="API_Caixa_Diario", lifespan=lifespan)

app.include_router(transform.router)