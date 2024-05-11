from pydantic import BaseModel

from common.database.entity import Contract
from common.model.types import Address


class ContractRequest(BaseModel):
    address: Address


class ContractResponse(BaseModel):
    address: Address
    status: Contract.Status
    source: str | None
