from concurrent import futures
import grpc
from google.protobuf.any_pb2 import Any

from proto.math_pb2 import MathError
from proto.math_pb2_grpc import MathServiceServicer, add_MathServiceServicer_to_server
import time


class MathService(MathServiceServicer):
    def add(self, request, context):
        details = Any()
        details.Pack(MathError(message="salam!"))
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        context.set_details(details.SerializeToString())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_MathServiceServicer_to_server(MathService(), server)

    server.add_insecure_port('[::]:8000')
    server.start()

    print('started server on [::]:8000')

    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
