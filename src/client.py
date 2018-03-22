import grpc
from google.protobuf.any_pb2 import Any
from google.protobuf.struct_pb2 import Struct

from proto.math_pb2 import Value
from proto.math_pb2_grpc import MathServiceStub


def run():
    channel = grpc.insecure_channel('app:8000')
    stub = MathServiceStub(channel)

    try:
        print(stub.add(iter([Value(value=x) for x in range(10)])))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()
