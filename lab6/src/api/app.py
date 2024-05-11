from fastapi import FastAPI

from api.controller.middleware.exception import ExceptionMiddleware
from api.controller.middleware.logging import LoggingMiddleware
from api.controller.middleware.prometheus import PrometheusMiddleware
from api.controller.middleware.tracing import TracingMiddleware
from api.controller.routers import contracts, metrics, test
from common.config.logging import LoggingConfig
from common.config.tracing import TracingConfig

LoggingConfig().setup_logging()
TracingConfig().setup_tracing({"service.name": "api"})

app = FastAPI()

app.include_router(contracts.router)
app.include_router(test.router)
app.include_router(metrics.router)

app.add_middleware(ExceptionMiddleware, app_name="api")
app.add_middleware(LoggingMiddleware)
app.add_middleware(PrometheusMiddleware, app_name="api")
app.add_middleware(TracingMiddleware)
