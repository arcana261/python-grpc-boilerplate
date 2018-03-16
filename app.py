from concurrent import futures
import grpc
import signal
import time

import settings
from proto.math_pb2_grpc import add_MathServicer_to_server
from servicer import Math
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
    logger.info('starting server on environment {}'.format(settings.env))
    for setting in settings:
        logger.info('{} = {}'.format(setting, getattr(settings, setting)))

    killer = GracefulKiller()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    add_MathServicer_to_server(Math(), server)

    server.add_insecure_port('[::]:{}'.format(settings.PORT))
    server.start()

    logger.info('started server on [::]:{}'.format(settings.PORT))

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
