from enum import Enum

import sqlalchemy as db
from opentelemetry import trace
from sqlalchemy import TypeDecorator

from common.database.entity import BaseEntity
from common.utils.tracing import observed

tracer = trace.get_tracer(__name__)


class AddressEncoder(TypeDecorator):
    impl = db.BINARY
    cache_ok = True

    @observed(tracer)
    def process_bind_param(self, value: bytes | str, dialect):
        if isinstance(value, bytes):
            return value.hex().encode()
        if isinstance(value, str):
            return bytes.fromhex(value[2:])
        return None

    @observed(tracer)
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
