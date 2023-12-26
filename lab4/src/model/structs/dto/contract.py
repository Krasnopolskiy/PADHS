from typing import Annotated

from pydantic import BaseModel, Field

from database.entity.contract import Contract

Address = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{40}$")]


class ContractRequest(BaseModel):
    address: Address


class ContractResponse(BaseModel):
    address: Address
    status: Contract.Status
    source: str | None
