from random import randint

from snapshot import Snapshot


class UniformSample(object):
    BITS_PER_LONG = 63
    values = []

    def __init__(self, reservoir_size):
        self.values = [0 for x in xrange(reservoir_size)]
        self.clear()

    def clear(self):
        self.values = [0 for x in xrange(len(self.values))]
        self.count = 0

    def size(self):
        if self.count > len(self.values):
            return len(self.values)
        return self.count

    def update(self, value):
        self.count += 1
        if self.count <= len(self.values):
            self.values[self.count - 1] = value
        else:
            r = UniformSample.next_long(self.count)
            if r < len(self.values):
                self.values[r] = value

    @classmethod
    def next_long(klass, n):
        return randint(0, n-1)

    def get_snapshot(self):
        copy = []
        for i in xrange(self.size()):
            copy.append(self.values[i])
        return Snapshot(copy)
