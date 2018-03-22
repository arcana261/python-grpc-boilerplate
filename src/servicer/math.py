from proto.math_pb2 import Result
from proto.math_pb2_grpc import MathServicer
from util import getLogger

logger = getLogger(__name__)


class Math(MathServicer):
    def add(self, request_iterator, context):
        result = 0.0
        logger.info('add got called!')
        for request in request_iterator:
            if not context.is_active():
                break
            logger.info('read {} from input!'.format(request.value))
            result = result + request.value
        logger.info('add result is {}'.format(result))
        return Result(result=result)

    def fibonachi_stream(self, request_iterator, context):
        a, b = 0, 1

        logger.info('fibonachi stream called!')

        for request in request_iterator:
            if not context.is_active():
                break

            logger.info('request to write {}!'.format(request.count))

            for _ in range(request.count):
                if not context.is_active():
                    break

                logger.info('returning result: {}'.format(a))
                yield Result(result=a)

                a, b = b, a + b

        logger.info('end fibonachi stream!')
