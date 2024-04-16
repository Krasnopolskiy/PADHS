from aio_pika import Message
from opentelemetry import trace

from common.amqp.base import BaseAMQPProducer
from common.amqp.dto.contract import ContractDto
from common.amqp.session import Queue
from common.utils.tracing import aobserved

tracer = trace.get_tracer(__name__)


class ContractProducer(BaseAMQPProducer):
    queue = Queue.CONTRACT

    @aobserved(tracer)
    async def publish(self, request: ContractDto):
        message = Message(body=request.model_dump_json().encode())
        await self.queue.publish(self.channel, message)
