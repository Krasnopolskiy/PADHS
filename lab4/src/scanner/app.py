import asyncio

import structlog

from common.config.logging import LoggingConfig
from scanner.contract import ContractScanner

LoggingConfig().setup_logging()

logger = structlog.get_logger()


def main():
    logger.info("Start scanning contracts")
    scanner = ContractScanner()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(scanner.start())


if __name__ == "__main__":
    main()
