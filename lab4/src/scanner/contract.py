import asyncio
import json
from asyncio import sleep

import structlog
from aio_pika import IncomingMessage
from mimesis import Locale, Text

from common.amqp.consumer.contract import ContractConsumer
from common.amqp.dto.contract import ContractDto
from common.database.dao.contract import ContractDao
from common.database.entity import Contract
from common.model.mapper.contract import ContractMapper

logger = structlog.get_logger()


class ContractScanner:
    delay = 1
    bandwidth = 100
    source_length = 10

    def __init__(self):
        self.consumer = ContractConsumer
        self.generator = Text(Locale.EN)
        self.mapper = ContractMapper()
        self.semaphore = asyncio.BoundedSemaphore(self.bandwidth)
        self.dao: ContractDao | None = None

    async def scan(self, contract: Contract):
        await sleep(self.delay)
        contract.source = self.generator.text(self.source_length)
        await self.dao.save(contract)

    async def update_status(self, contract: Contract, status: Contract.Status):
        contract.status = status
        await self.dao.save(contract)

    async def process(self, dto: ContractDto):
        async with self.semaphore:
            logger.info("Processing [%s]: started", dto.address)
            contract = await self.dao.find_by_address(dto.address)
            await self.update_status(contract, Contract.Status.PROCESS)
            await self.scan(contract)
            await self.update_status(contract, Contract.Status.SUCCESS)
            logger.info("Processing [%s]: success", dto.address)

    async def callback(self, message: IncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())
            contract = ContractDto(**body)
            asyncio.create_task(self.process(contract))

    async def start(self):
        self.dao = ContractDao()
        await self.consumer.start(self.callback)
