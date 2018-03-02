from concurrent import futures
import grpc
import signal
from google.protobuf.any_pb2 import Any

from proto.math_pb2 import MathError, AddResponse
from proto.math_pb2_grpc import MathServiceServicer, add_MathServiceServicer_to_server
import time


class MathService(MathServiceServicer):
    def add(self, request, context):
        return AddResponse(result=request.x + request.y)


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def serve():
    killer = GracefulKiller()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_MathServiceServicer_to_server(MathService(), server)

    server.add_insecure_port('[::]:8000')
    server.start()

    print('started server on [::]:8000')

    try:
        while not killer.kill_now:
            time.sleep(1)
        server.stop(0)
    except KeyboardInterrupt:
        server.stop(0)
    finally:
        print('sayonara! :)')


if __name__ == '__main__':
    serve()
