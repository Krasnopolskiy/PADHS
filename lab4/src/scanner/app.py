import asyncio

import structlog

from scanner.contract import ContractScanner

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%H:%M:%S", utc=False),
        structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)
logger = structlog.get_logger()


def main():
    logger.info("Start scanning contracts")
    scanner = ContractScanner()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(scanner.start())


if __name__ == "__main__":
    main()
