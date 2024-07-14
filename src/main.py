from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api_v1 import router as router_api_v1
from src.api_v1.routers.parkins_router import router as parking
from src.api_v1.routers.client_parking_router import router as client_parking
from src.api_v1.routers.client_router import router as client
from src.core.config import settings
from src.core.database.base import Base
from src.core.database.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    if db_helper.engine is not None:
        await db_helper.engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,  # ускоренный json
)

app.include_router(router_api_v1)
# app.include_router(router=client, prefix=settings.api_vi_prefix)
# app.include_router(router=parking, prefix=settings.api_vi_prefix)
# app.include_router(router=client_parking, prefix=settings.api_vi_prefix)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
