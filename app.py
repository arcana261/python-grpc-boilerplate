from concurrent import futures
import grpc
import signal
from proto.math_pb2_grpc import add_MathServiceServicer_to_server
from servicer import MathServicer
import time
from util import getLogger

logger = getLogger(__name__)


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def serve():
    killer = GracefulKiller()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    add_MathServiceServicer_to_server(MathServicer(), server)

    server.add_insecure_port('[::]:8000')
    server.start()

    logger.info('started server on [::]:8000')

    try:
        while not killer.kill_now:
            time.sleep(1)
        server.stop(0)
    except KeyboardInterrupt:
        server.stop(0)
    finally:
        logger.info('sayonara! :)')


if __name__ == '__main__':
    serve()
