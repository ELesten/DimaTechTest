from fastapi import FastAPI

from app.api.routers.payment_router import payment_router
from app.api.routers.user_router import user_router
from app.api.routers.auth_router import auth_router
from app.api.routers.wallet_router import wallet_router
from app.utils.description import description

app = FastAPI(
    title="DimoTech test task",
    description=description,
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(wallet_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
