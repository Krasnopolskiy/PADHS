import logging

from common.amqp.base import BaseAMQPConsumer
from common.amqp.session import Queue

logger = logging.getLogger(__name__)


class ContractConsumer(BaseAMQPConsumer):
    queue = Queue.CONTRACT
