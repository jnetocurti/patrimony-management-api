from fastapi import FastAPI

from app.api import (
    assets,
    asset_types,
    event_types,
    subscriptions,
    currency_types
)
from app.core import settings, connection
from app.core.business import ensure_indexes

app = FastAPI()
app.include_router(assets.router)
app.include_router(subscriptions.router)
app.include_router(asset_types.router)
app.include_router(event_types.router)
app.include_router(currency_types.router)


@app.on_event("startup")
async def event_startup():
    connection.connect()
    await ensure_indexes()


@app.on_event("shutdown")
async def event_shutdown():
    connection.close()


@app.get("/info", include_in_schema=False)
async def info():
    return {
        "appName": settings.app_name,
        "appVersion": settings.app_version
    }
