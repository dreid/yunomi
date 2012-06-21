class Counter(object):

    def __init__(self):
        self._count = 0

    def inc(self, n = 1):
        self._count += n

    def dec(self, n = 1):
        self._count -= n

    def get_count(self):
        return self._count

    def clear(self):
        self._count = 0
