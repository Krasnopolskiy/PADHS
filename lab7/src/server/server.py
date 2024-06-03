import logging
import time
from concurrent import futures

import grpc

from proto import hello_pb2, hello_pb2_grpc

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


class HelloService(hello_pb2_grpc.HelloServiceServicer):
    def __init__(self, name: str):
        self.name = name

    def say_hello(self, request, context):
        logger.info(f"Incoming: {request}")

        message = f"{self.name}: Hello from {self.name}, {request.name}"

        logger.info(f"Outcoming: {message}")

        return hello_pb2.HelloReply(message=message)


def serve(server_name: str, port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_service = HelloService(server_name)
    hello_pb2_grpc.add_HelloServiceServicer_to_server(hello_service, server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info(f"Server {server_name} started on port {port}")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


def main():
    import sys

    name = sys.argv[1]
    port = int(sys.argv[2])
    serve(name, port)


if __name__ == "__main__":
    main()
