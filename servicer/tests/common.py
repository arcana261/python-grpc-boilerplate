
class FakeContext:
    def __init__(self):
        pass

    def is_active(self):
        raise NotImplemented


class FakeIterator:
    def __init__(self):
        self._stack = []

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if len(self._stack) < 1:
            raise StopIteration

        return self._stack.pop(0)
