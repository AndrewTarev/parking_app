from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api_v1 import router as router_api_v1


app = FastAPI(default_response_class=ORJSONResponse)  # ускоренный json

app.include_router(router_api_v1)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
