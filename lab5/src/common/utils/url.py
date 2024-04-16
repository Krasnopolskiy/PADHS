from fastapi.requests import Request
from fastapi.routing import Match


def get_path(request: Request) -> tuple[str, bool]:
    for route in request.app.routes:
        match, child_scope = route.matches(request.scope)
        if match == Match.FULL:
            return route.path, True

    return request.url.path, False
