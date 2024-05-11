from asyncio import sleep

from fastapi import Depends
from opentelemetry import trace

from api.model.schemas.contract import ContractRequest, ContractResponse
from common.amqp.producer.contract import ContractProducer
from common.cache.constance import CONTRACT_CACHE_KEY, DEFAULT_LIFETIME
from common.cache.session import CacheConnectionManager
from common.database.dao.contract import ContractDao
from common.model.mapper.contract import ContractMapper
from common.model.types import Address
from common.utils.tracing import aobserved

tracer = trace.get_tracer(__name__)


class ContractService:
    mapper = ContractMapper()
    dao = ContractDao()

    def __init__(self, producer: ContractProducer = Depends(ContractProducer.get_producer)):
        self.producer = producer

    async def publish(self, request: ContractRequest):
        dto = self.mapper.request_as_dto(request)
        await self.producer.publish(dto)

    @aobserved(tracer)
    async def find_by_address(self, address: Address) -> ContractResponse:
        await sleep(0.05)
        contract = await self.dao.find_by_address(address)
        return self.mapper.entity_as_response(contract)

    @aobserved(tracer)
    async def find_by_address_cached(self, address: Address) -> ContractResponse:
        cache_key = CONTRACT_CACHE_KEY.format(address=address)
        with CacheConnectionManager() as connection:
            if contract := connection.get(cache_key):
                return ContractResponse.parse_raw(contract)

            contract = await self.dao.find_by_address(address)
            response = self.mapper.entity_as_response(contract)
            connection.set(cache_key, response.model_dump_json(), DEFAULT_LIFETIME)
        return response

    @aobserved(tracer)
    async def create(self, request: ContractRequest) -> ContractResponse:
        contract = await self.dao.find_by_address_or_none(request.address)
        if contract is None:
            contract = await self.dao.save(self.mapper.request_as_entity(request))
            await self.publish(request)
        return self.mapper.entity_as_response(contract)
