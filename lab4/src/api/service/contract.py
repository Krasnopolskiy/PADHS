from fastapi import Depends

from api.model.schemas.contract import ContractRequest, ContractResponse
from common.amqp.producer.contract import ContractProducer
from common.database.dao.contract import ContractDao
from common.model.mapper.contract import ContractMapper
from common.model.types import Address


class ContractService:
    def __init__(
        self,
        dao: ContractDao = Depends(),
        mapper: ContractMapper = Depends(),
        producer: ContractProducer = Depends(ContractProducer.get_producer),
    ):
        self.dao = dao
        self.mapper = mapper
        self.producer = producer

    async def find_by_address(self, address: Address) -> ContractResponse:
        contract = await self.dao.find_by_address(address)
        return self.mapper.entity_as_response(contract)

    async def create(self, request: ContractRequest) -> ContractResponse:
        contract = await self.dao.find_by_address_or_none(request.address)
        if contract is None:
            contract = await self.dao.save(self.mapper.request_as_entity(request))
            await self.producer.publish(self.mapper.request_as_dto(request))
        return self.mapper.entity_as_response(contract)
