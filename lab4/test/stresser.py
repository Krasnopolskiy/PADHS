import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from secrets import token_hex

import structlog
from aiohttp import ClientSession
from structlog.processors import CallsiteParameter

from api.model.schemas.contract import ContractRequest, ContractResponse
from common.database.entity import Contract
from common.model.types import Address

URL = "http://localhost:8000/contracts"
RPS = 25
DURATION = 1 * 60

structlog.configure(
    processors=[
        structlog.processors.CallsiteParameterAdder(parameters=[CallsiteParameter.PROCESS_NAME]),
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%H:%M:%S", utc=False),
        # structlog.dev.ConsoleRenderer(),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)
logger = structlog.get_logger()


def generate_address() -> str:
    return f"0x{token_hex(20)}"


def is_finished(contracts: dict[Address, Contract.Status], address: Address) -> bool:
    return contracts[address] in {Contract.Status.SUCCESS, Contract.Status.ERROR}


def ignore_exceptions(func):
    async def wrapper(*args, **kwargs):
        while True:
            try:
                return await func(*args, **kwargs)
            except Exception:
                pass

    return wrapper


@ignore_exceptions
async def create_contract(session: ClientSession) -> dict:
    request = ContractRequest(address=generate_address())
    async with session.post(f"{URL}/", json=request.model_dump()) as response:
        return await response.json()


@ignore_exceptions
async def fetch_contract(session: ClientSession, address: Address) -> dict | None:
    async with session.get(f"{URL}/{address}") as response:
        if response.status == 200:
            return await response.json()
    return None


async def create_bulk_contracts(contracts: dict[Address, Contract.Status]):
    async with ClientSession() as session:
        start_time = time.time()
        while time.time() - start_time < DURATION:
            logger.info("Creating: [%s]", RPS)
            request_time = time.time()
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(create_contract(session)) for _ in range(RPS)]
            for task in tasks:
                response = ContractResponse(**task.result())
                contracts[response.address] = response.status
            while time.time() - request_time < 1:
                await asyncio.sleep(0.01)


async def fetch_bulk_contracts(contracts: dict[Address, Contract.Status]):
    while not contracts:
        await asyncio.sleep(1)
    async with ClientSession() as session:
        while any(not is_finished(contracts, address) for address in contracts.keys()):
            pending = [address for address in contracts.keys() if not is_finished(contracts, address)]
            logger.info("Pending: [%s]", len(pending))
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(fetch_contract(session, address)) for address in pending]
            for task in tasks:
                if response := task.result():
                    response = ContractResponse(**response)
                    contracts[response.address] = response.status
            await asyncio.sleep(1)


async def launch():
    contracts: dict[Address, Contract.Status] = {}
    start = time.time()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(create_bulk_contracts(contracts))
        tg.create_task(fetch_bulk_contracts(contracts))
    logger.info("Elapsed: [%s]", time.time() - start)


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(launch())


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(main) for _ in range(4)]
        for future in futures:
            future.result()
