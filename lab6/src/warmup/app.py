import asyncio

import structlog

from common.cache.constance import CONTRACT_CACHE_KEY, DEFAULT_LIFETIME
from common.cache.session import CacheConnectionManager
from common.config.logging import LoggingConfig
from common.database.dao.contract import ContractDao
from common.database.entity import Contract
from common.model.mapper.contract import ContractMapper

LoggingConfig().setup_logging()

dao = ContractDao()
mapper = ContractMapper()

logger = structlog.get_logger()


def save_to_cache(contract: Contract):
    contract_response = mapper.entity_as_response(contract)
    cache_key = CONTRACT_CACHE_KEY.format(address=contract.address)
    with CacheConnectionManager() as connection:
        connection.set(cache_key, contract_response.model_dump_json(), DEFAULT_LIFETIME)


async def main():
    logger.info("Warmup started")
    for contract in await dao.find_processed():
        logger.info("Caching %s", contract.address)
        save_to_cache(contract)
    logger.info("Warmup finished")


if __name__ == "__main__":
    asyncio.run(main())
