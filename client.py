import grpc

from proto.math_pb2 import AddRequest
from proto.math_pb2_grpc import MathServiceStub


def run():
    channel = grpc.insecure_channel('app:8000')
    stub = MathServiceStub(channel)

    print(stub.add(AddRequest(x=3, y=6)))


if __name__ == '__main__':
    run()
