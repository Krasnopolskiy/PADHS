from time import sleep

import structlog
from mimesis import Internet, Locale, Numeric, Text

from api.model.schemas.test import LogLevel, RandomLogResponse, RandomSleepResponse, RandomStatusResponse

logger = structlog.get_logger(__name__)


class TestingService:
    def __init__(self):
        self.text_generator = Text(Locale.EN)
        self.internet_generator = Internet()
        self.number_generator = Numeric()

    def status(self):
        code, message = self.internet_generator.http_status_message().split(" ", 1)
        return RandomStatusResponse(status=int(code), message=message)

    def sleep(self):
        time = self.number_generator.integer_number(start=2, end=5)
        sleep(time)
        return RandomSleepResponse(sleep=time)

    def log(self, level: LogLevel):
        message = self.text_generator.sentence()
        level.log(message)
        return RandomLogResponse(level=level, message=message)

    def error(self):
        message = self.text_generator.sentence()
        raise Exception(message)
