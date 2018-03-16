from unittest import TestCase
from unittest.mock import MagicMock

from proto.math_pb2 import Value, More
from servicer import Math

from servicer.tests.common import FakeContext


class TestMath(TestCase):
    def test_add(self):
        s = Math()
        context = FakeContext()
        context.is_active = MagicMock(return_value=True)
        result = s.add(map(lambda v: Value(value=v), [1, 5, -1, 6]), context)
        self.assertEqual(result.result, 11)

    def test_fibonachi_stream(self):
        s = Math()
        context = FakeContext()
        context.is_active = MagicMock(return_value=True)
        result = list(s.fibonachi_stream([More(count=2), More(count=3)], context))
        self.assertListEqual(list(x.result for x in result), [0, 1, 1, 2, 3])
