from enum import Enum

import structlog
from pydantic import BaseModel

logger = structlog.get_logger(__name__)


class LogLevel(str, Enum):
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"

    def log(self, message):
        match self:
            case LogLevel.debug:
                logger.debug(message)
            case LogLevel.info:
                logger.info(message)
            case LogLevel.warning:
                logger.warning(message)
            case LogLevel.error:
                logger.error(message)
            case LogLevel.critical:
                logger.critical(message)


class RandomStatusResponse(BaseModel):
    status: int
    message: str


class RandomSleepResponse(BaseModel):
    sleep: int


class RandomLogResponse(BaseModel):
    level: LogLevel
    message: str
