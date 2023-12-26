from fastapi import Depends
from sqlalchemy.orm import Session

from database.entity.contract import Contract
from database.session import get_db_session
from model.structs.dto.contract import Address
from model.structs.exceptions.common import ResourceNotFoundException


class ContractDao:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def save(self, contract: Contract) -> Contract:
        self.session.add(contract)
        self.session.commit()
        self.session.refresh(contract)
        return contract

    def find_by_address_or_none(self, address: Address) -> Contract:
        return self.session.query(Contract).get(address)

    def find_by_address(self, address: Address) -> Contract:
        entity = self.find_by_address_or_none(address)
        if entity is None:
            raise ResourceNotFoundException()
        return entity
