import logging

import structlog
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from structlog.types import EventDict, Processor


def rename_event_key(_, __, event_dict: EventDict) -> EventDict:
    event_dict["message"] = event_dict.pop("event")
    return event_dict


def drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
    event_dict.pop("color_message", None)
    return event_dict


class LoggingConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    log_level: str = Field(alias="LOG_LEVEL")

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        drop_color_message_key,
        rename_event_key,
    ]

    def console_handler(self):
        formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=self.shared_processors,
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(),
            ],
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    def setup_logging(self):
        structlog.configure(
            processors=self.shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        root_logger = logging.getLogger()
        root_logger.addHandler(self.console_handler())
        root_logger.setLevel(self.log_level.upper())

        for _log in ["uvicorn", "uvicorn.error"]:
            logging.getLogger(_log).handlers.clear()
            logging.getLogger(_log).propagate = True

        logging.getLogger("uvicorn.access").handlers.clear()
        logging.getLogger("uvicorn.access").propagate = False
        logging.getLogger("urllib3").setLevel(logging.INFO)
