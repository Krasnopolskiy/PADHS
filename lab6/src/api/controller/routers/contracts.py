from fastapi import APIRouter, Depends, Path

from api.model.schemas.contract import ContractRequest, ContractResponse
from api.service.contract import ContractService
from common.model.types import Address

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.post("/")
async def create(request: ContractRequest, service: ContractService = Depends()) -> ContractResponse:
    return await service.create(request)


@router.get("/{address}")
async def find_by_address(address: Address = Path(), service: ContractService = Depends()) -> ContractResponse:
    return await service.find_by_address(address)


@router.get("/cached/{address}")
async def find_by_address_cached(address: Address = Path(), service: ContractService = Depends()) -> ContractResponse:
    return await service.find_by_address_cached(address)
