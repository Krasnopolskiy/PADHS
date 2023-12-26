from database.entity.contract import Contract
from model.structs.dto.contract import ContractResponse, ContractRequest


class ContractMapper:
    def as_entity(self, request: ContractRequest) -> Contract:
        return Contract(
            address=request.address,
        )

    def as_response(self, contract: Contract) -> ContractResponse:
        return ContractResponse(
            address=contract.address,
            status=contract.status,
            source=contract.source,
        )
