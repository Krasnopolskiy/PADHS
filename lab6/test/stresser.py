import asyncio
import time
from random import choice
from secrets import token_hex

import structlog
from aiohttp import ClientSession
from structlog.processors import CallsiteParameter

from api.model.schemas.contract import ContractRequest, ContractResponse
from common.database.entity import Contract
from common.model.types import Address

RPS = 5
DURATION = 5 * 60

URL = "http://localhost:8000"
TESTING_ENDPOINTS = (
    "status",
    # "sleep",
    "log/debug",
    "log/info",
    "log/warning",
    # "log/error",
    # "log/critical",
    # "error",
)


structlog.configure(
    processors=[
        structlog.processors.CallsiteParameterAdder(parameters=[CallsiteParameter.PROCESS_NAME]),
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%H:%M:%S", utc=False),
        structlog.dev.ConsoleRenderer(),
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
async def create_contract(session: ClientSession) -> ContractResponse | None:
    request = ContractRequest(address=generate_address())
    async with session.post(f"{URL}/contracts", json=request.model_dump()) as response:
        if response.status == 200:
            data = await response.json()
            return ContractResponse(**data)
    return None


@ignore_exceptions
async def fetch_contract(session: ClientSession, address: Address) -> ContractResponse | None:
    path = "contracts/cached" if choice([True, False]) else "contracts"
    async with session.get(f"{URL}/{path}/{address}") as response:
        if response.status == 200:
            data = await response.json()
            return ContractResponse(**data)
    return None


@ignore_exceptions
async def call_random_endpoint(session: ClientSession):
    endpoint = choice(TESTING_ENDPOINTS)
    async with session.get(f"{URL}/test/{endpoint}") as response:
        await response.json()


async def create_bulk_contracts(contracts: dict[Address, Contract.Status]):
    async with ClientSession() as session:
        start_time = time.time()
        while time.time() - start_time < DURATION:
            logger.info("Creating: [%s]", RPS)
            request_time = time.time()
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(create_contract(session)) for _ in range(RPS)]
            for task in tasks:
                if response := task.result():
                    contracts[response.address] = response.status
            while time.time() - request_time < 1:
                await asyncio.sleep(0.01)


async def fetch_bulk_contracts(contracts: dict[Address, Contract.Status]):
    while not contracts:
        await asyncio.sleep(1)
    async with ClientSession() as session:
        while any(not is_finished(contracts, address) for address in contracts.keys()):
            pending = [address for address in contracts.keys() if not is_finished(contracts, address)]
            logger.info("Fetching: [%s]", len(pending))
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(fetch_contract(session=session, address=address)) for address in pending[:RPS]]
            for task in tasks:
                if response := task.result():
                    contracts[response.address] = response.status
            await asyncio.sleep(1)


async def call_random_endpoints():
    async with ClientSession() as session:
        start_time = time.time()
        while time.time() - start_time < DURATION:
            logger.info("Testing: [%s]", RPS)
            request_time = time.time()
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(call_random_endpoint(session)) for _ in range(RPS)]
            for task in tasks:
                task.result()
            while time.time() - request_time < 1:
                await asyncio.sleep(0.01)


async def launch():
    contracts: dict[Address, Contract.Status] = {}
    start = time.time()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(create_bulk_contracts(contracts))
        tg.create_task(fetch_bulk_contracts(contracts))
        tg.create_task(call_random_endpoints())
    logger.info("Elapsed: [%s]", time.time() - start)


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(launch())


if __name__ == "__main__":
    main()
