from fastapi import Depends

from database.dao.contract import ContractDao
from model.mapper.contract import ContractMapper
from model.structs.dto.contract import Address, ContractRequest, ContractResponse


class ContractService:
    def __init__(self, dao: ContractDao = Depends(), mapper: ContractMapper = Depends()):
        self.dao = dao
        self.mapper = mapper

    def find_by_address(self, address: Address) -> ContractResponse:
        contract = self.dao.find_by_address(address)
        return self.mapper.as_response(contract)

    def create(self, request: ContractRequest) -> ContractResponse:
        contract = self.dao.find_by_address_or_none(request.address)
        if contract is None:
            contract = self.mapper.as_entity(request)
            contract = self.dao.save(contract)
        return self.mapper.as_response(contract)
