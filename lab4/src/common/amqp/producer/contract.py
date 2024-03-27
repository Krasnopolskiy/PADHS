from aio_pika import Message

from common.amqp.base import BaseAMQPProducer
from common.amqp.dto.contract import ContractDto
from common.amqp.session import Queue


class ContractProducer(BaseAMQPProducer):
    queue = Queue.CONTRACT

    async def publish(self, request: ContractDto):
        message = Message(body=request.model_dump_json().encode())
        await self.queue.publish(self.channel, message)
