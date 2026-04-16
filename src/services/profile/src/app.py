from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream import FastStream
from starlette.middleware.cors import CORSMiddleware

from src.core.infrastructures import rmq_broker, postgresql
from src.schema import *
from src.api import router

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await postgresql.init(metadata, clear_db=False)
    await rmq_broker.start()
    yield
    await rmq_broker.broker.stop()

app = FastAPI(lifespan=lifespan)

faststream_app = FastStream(rmq_broker.broker)
# StandaloneDocs(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(router)
