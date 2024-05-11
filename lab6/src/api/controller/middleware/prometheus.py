import re
import time

from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from api.controller.metrics import INFO, REQUESTS, REQUESTS_IN_PROGRESS, REQUESTS_PROCESSING_TIME, RESPONSES
from common.utils.tracing import aobserved
from common.utils.url import get_path

tracer = trace.get_tracer(__name__)


class PrometheusMiddleware(BaseHTTPMiddleware):
    ignored = (
        re.compile(r"/metrics.*"),
        re.compile(r"/docs.*"),
    )

    def __init__(self, app: ASGIApp, app_name: str) -> None:
        super().__init__(app)
        self.app_name = app_name
        INFO.labels(app_name=self.app_name).inc()

    def is_ignored(self, path: str) -> bool:
        for pattern in self.ignored:
            if pattern.match(path):
                return True
        return False

    async def measure(self, method: str, path: str, request: Request, call_next: RequestResponseEndpoint) -> Response:
        REQUESTS_IN_PROGRESS.labels(method=method, path=path, app_name=self.app_name).inc()
        REQUESTS.labels(method=method, path=path, app_name=self.app_name).inc()

        start_time = time.perf_counter()
        response = await call_next(request)
        after_time = time.perf_counter()

        span = trace.get_current_span()
        trace_id = trace.format_trace_id(span.get_span_context().trace_id)
        status_code = response.status_code

        REQUESTS_PROCESSING_TIME.labels(method=method, path=path, app_name=self.app_name).observe(
            after_time - start_time, exemplar={"TraceID": trace_id}
        )
        RESPONSES.labels(method=method, path=path, status_code=status_code, app_name=self.app_name).inc()
        REQUESTS_IN_PROGRESS.labels(method=method, path=path, app_name=self.app_name).dec()

        return response

    @aobserved(tracer)
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        method = request.method
        path, is_handled_path = get_path(request)

        if not is_handled_path:
            return await call_next(request)

        if self.is_ignored(path):
            return await call_next(request)

        return await self.measure(method, path, request, call_next)
