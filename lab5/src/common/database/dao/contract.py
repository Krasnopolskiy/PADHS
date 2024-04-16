from opentelemetry import trace

from common.database.entity import Contract
from common.database.session import DatabaseSessionManager
from common.model.exceptions.common import ResourceNotFoundException
from common.model.types import Address
from common.utils.tracing import aobserved

tracer = trace.get_tracer(__name__)


class ContractDao:
    @aobserved(tracer)
    async def save(self, contract: Contract) -> Contract:
        with DatabaseSessionManager() as session:
            session.add(contract)
            session.commit()
            session.refresh(contract)
        return contract

    @aobserved(tracer)
    async def find_by_address_or_none(self, address: Address) -> Contract:
        with DatabaseSessionManager() as session:
            return session.query(Contract).get(address)

    @aobserved(tracer)
    async def find_by_address(self, address: Address) -> Contract:
        entity = await self.find_by_address_or_none(address)
        if entity is None:
            raise ResourceNotFoundException()
        return entity
