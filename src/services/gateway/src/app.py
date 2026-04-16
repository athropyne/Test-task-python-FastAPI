from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from faststream import FastStream
from starlette.middleware.cors import CORSMiddleware

from src.core.infrastructures import rmq_broker, postgresql
from src.schema import *
from src.services.account.api import account_router
from src.services.cart.api import cart_router
from src.services.order.api import order_router
from src.services.product.api import product_router
from src.services.profile.api import profile_router

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
router = APIRouter(prefix="/api")
router.include_router(account_router)
router.include_router(profile_router)
router.include_router(product_router)
router.include_router(cart_router)
router.include_router(order_router)
app.include_router(router)
