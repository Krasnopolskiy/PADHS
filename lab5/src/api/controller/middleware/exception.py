import structlog
from fastapi.exception_handlers import http_exception_handler
from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from api.controller.metrics import EXCEPTIONS
from common.model.exceptions.common import InternalServerException
from common.utils.tracing import aobserved

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)


class ExceptionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, app_name: str):
        self.app_name = app_name
        super().__init__(app)

    @aobserved(tracer)
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            EXCEPTIONS.labels(
                method=request.method,
                path=request.url.path,
                exception_type=type(exc).__name__,
                app_name=self.app_name,
            ).inc()
            logger.exception(exc)
            return await http_exception_handler(request, InternalServerException())
