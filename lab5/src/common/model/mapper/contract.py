from api.model.schemas.contract import ContractRequest, ContractResponse
from common.amqp.dto.contract import ContractDto
from common.database.entity.contract import Contract


class ContractMapper:
    def request_as_entity(self, request: ContractRequest) -> Contract:
        return Contract(
            address=request.address,
        )

    def request_as_dto(self, request: ContractRequest) -> ContractDto:
        return ContractDto(
            address=request.address,
        )

    def dto_as_response(self, dto: ContractDto) -> ContractResponse:
        return ContractResponse(
            address=dto.address,
            status=dto.status,
            source=dto.source,
        )

    def entity_as_response(self, contract: Contract) -> ContractResponse:
        return ContractResponse(
            address=contract.address,
            status=contract.status,
            source=contract.source,
        )
