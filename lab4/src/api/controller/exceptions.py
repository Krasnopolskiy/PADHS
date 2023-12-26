import logging

from fastapi.exception_handlers import http_exception_handler
from fastapi.requests import Request

from model.structs.exceptions.common import InternalServerException

logger = logging.getLogger(__name__)


async def exception_handler(request: Request, exc: Exception):
    logger.error(exc)
    return await http_exception_handler(request, InternalServerException())
