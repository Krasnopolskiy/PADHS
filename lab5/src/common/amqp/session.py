from enum import Enum
from sqlite3 import Connection

from aio_pika import Channel, Message, connect_robust
from aio_pika.abc import AbstractRobustChannel
from opentelemetry import trace

from common.config.amqp import AMQPSettings
from common.utils.tracing import aobserved

tracer = trace.get_tracer(__name__)


class AMQPSessionManager:
    def __init__(self):
        self.url = AMQPSettings().url
        self.connection: Connection | None = None
        self.channel: Channel | None = None

    async def __aenter__(self) -> AbstractRobustChannel:
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.channel.connection = self.channel.channel.connection
        return self.channel

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.channel is not None:
            await self.channel.close()
        if self.connection is not None:
            await self.connection.close()


class Queue(str, Enum):
    CONTRACT = "CONTRACT"

    async def declare(self, channel: AbstractRobustChannel):
        return await channel.declare_queue(self.value)

    @aobserved(tracer)
    async def publish(self, channel: AbstractRobustChannel, message: Message):
        await channel.default_exchange.publish(message, routing_key=self.value)
