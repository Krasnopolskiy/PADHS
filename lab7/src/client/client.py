import logging
import time
from time import sleep

import grpc

from proto import hello_pb2, hello_pb2_grpc

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def run():
    while True:
        start_time = time.time()
        with grpc.insecure_channel("lb:8080") as channel:
            stub = hello_pb2_grpc.HelloServiceStub(channel)
            response = stub.say_hello(hello_pb2.HelloRequest(name="client"))
        end_time = time.time()
        logger.info(f"{end_time - start_time}: {response.message}")
        sleep(1)


if __name__ == "__main__":
    run()
