from proto.math_pb2 import Result
from proto.math_pb2_grpc import MathServiceServicer
from util import getLogger

logger = getLogger(__name__)


class MathServicer(MathServiceServicer):
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
