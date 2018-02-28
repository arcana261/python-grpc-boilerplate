import grpc
from google.protobuf.any_pb2 import Any

from proto.math_pb2 import AddRequest, MathError
from proto.math_pb2_grpc import MathServiceStub


def run():
    channel = grpc.insecure_channel('app:8000')
    stub = MathServiceStub(channel)

    try:
        print(stub.add(AddRequest(x=3, y=6)))
    except Exception as e:
        code = e.code()
        details = Any.FromString(bytearray(e.details(), 'ascii'))

        if (details.Is(MathError.DESCRIPTOR)):
            math_error = MathError()
            details.Unpack(math_error)
            print(math_error)
        else:
            print(e)


if __name__ == '__main__':
    run()
