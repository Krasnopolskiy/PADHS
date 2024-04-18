from fastapi import FastAPI

from api.controller.middleware.exception import ExceptionMiddleware
from api.controller.middleware.logging import LoggingMiddleware
from api.controller.routers import contracts
from common.config.logging import LoggingConfig

LoggingConfig().setup_logging()

app = FastAPI()

app.include_router(contracts.router)

app.add_middleware(ExceptionMiddleware, app_name="api")
app.add_middleware(LoggingMiddleware)
