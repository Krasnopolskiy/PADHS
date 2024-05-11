from typing import Any

from fastapi import HTTPException


class BaseApiException(HTTPException):
    status_code: int | None = None
    detail: Any | None = None
    headers: dict[str, str] | None = None

    def __init__(self):
        super().__init__(self.status_code, self.detail, self.headers)
