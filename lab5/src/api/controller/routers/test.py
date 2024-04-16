import structlog
from fastapi import APIRouter, Depends
from fastapi.responses import Response

from api.model.schemas.test import LogLevel, RandomLogResponse, RandomSleepResponse, RandomStatusResponse
from api.service.testing import TestingService

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/status")
async def random_status(response: Response, service: TestingService = Depends()) -> RandomStatusResponse:
    result = service.status()
    response.status_code = result.status
    return result


@router.get("/sleep")
async def random_sleep(service: TestingService = Depends()) -> RandomSleepResponse:
    return service.sleep()


@router.get("/log/{level}")
async def random_log(level: LogLevel, service: TestingService = Depends()) -> RandomLogResponse:
    return service.log(level)


@router.get("/error")
async def random_error(service: TestingService = Depends()) -> RandomLogResponse:
    return service.error()
