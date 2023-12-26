from enum import Enum

import sqlalchemy as db
from sqlalchemy import TypeDecorator

from database.entity.base import BaseEntity


class AddressEncoder(TypeDecorator):
    impl = db.BINARY
    cache_ok = True

    def process_bind_param(self, value: bytes | str, dialect):
        if isinstance(value, bytes):
            return value.hex().encode("utf-8")
        if isinstance(value, str):
            return bytes.fromhex(value[2:])
        return None

    def process_result_value(self, value: bytes, dialect):
        if value is None:
            return None
        return f"0x{value.hex()}"


class Contract(BaseEntity):
    __tablename__ = "contract"

    class Status(str, Enum):
        CREATED = "created"
        PROCESS = "process"
        SUCCESS = "success"
        ERROR = "error"

    address = db.Column(AddressEncoder(20), primary_key=True)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.CREATED)
    source = db.Column(db.Text(), nullable=True, default=None)
