from pydantic import BaseModel

from common.database.entity.contract import Contract
from common.model.types import Address


class ContractDto(BaseModel):
    address: Address
    status: Contract.Status | None = None
    source: str | None = None
