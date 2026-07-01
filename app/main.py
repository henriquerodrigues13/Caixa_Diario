from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

from app.routes import export, upload
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="API_Caixa_Diario", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(export.router)
app.include_router(upload.router)