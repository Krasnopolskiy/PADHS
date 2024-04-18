import structlog
from fastapi.exception_handlers import http_exception_handler
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from common.model.exceptions.common import InternalServerException

logger = structlog.get_logger(__name__)


class ExceptionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, app_name: str):
        self.app_name = app_name
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            logger.exception(exc)
            return await http_exception_handler(request, InternalServerException())
