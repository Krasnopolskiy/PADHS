from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from structlog import get_logger

from common.utils.tracing import aobserved

logger = get_logger(__name__)
tracer = trace.get_tracer(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    @aobserved(tracer)
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        logger.info("%s %s %s", request.method, request.url, response.status_code)
        return response
