from fastapi import APIRouter, Depends

from model.structs.dto.contract import ContractRequest, ContractResponse, Address
from service.contract import ContractService

router = APIRouter(prefix="/contract")


@router.post("/")
async def create(request: ContractRequest, service: ContractService = Depends()) -> ContractResponse:
    return service.create(request)


@router.get("/")
async def find_by_address(address: Address, service: ContractService = Depends()) -> ContractResponse:
    return service.find_by_address(address)
