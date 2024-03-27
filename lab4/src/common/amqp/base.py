import asyncio
from abc import ABC, abstractmethod
from typing import Callable, Coroutine

from aio_pika import IncomingMessage
from aio_pika.abc import AbstractRobustChannel

from common.amqp.session import AMQPSessionManager, Queue


class BaseAMQPProtocol(ABC):
    @property
    @abstractmethod
    def queue(self) -> Queue:
        pass


class BaseAMQPConsumer(BaseAMQPProtocol, ABC):
    bandwidth: int = 100

    def __init__(self, channel: AbstractRobustChannel):
        self.channel = channel

    async def start_consuming(self, callback: Callable[[IncomingMessage], Coroutine]):
        await self.channel.set_qos(self.bandwidth)
        queue = await self.queue.declare(self.channel)
        await queue.consume(callback)

    @classmethod
    async def start(cls, callback: Callable[[IncomingMessage], Coroutine]):
        async with AMQPSessionManager() as channel:
            consumer = cls(channel)
            await consumer.start_consuming(callback)
            await asyncio.Future()


class BaseAMQPProducer(BaseAMQPProtocol, ABC):
    def __init__(self, channel: AbstractRobustChannel):
        self.channel = channel

    @abstractmethod
    async def publish(self, message: str):
        pass

    @classmethod
    async def get_producer(cls):
        async with AMQPSessionManager() as channel:
            await cls.queue.declare(channel)
            yield cls(channel)
