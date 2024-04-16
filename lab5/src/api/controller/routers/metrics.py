from fastapi import APIRouter
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest
from starlette.requests import Request
from starlette.responses import Response

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/")
def metrics(request: Request) -> Response:
    return Response(generate_latest(REGISTRY), headers={"Content-Type": CONTENT_TYPE_LATEST})
