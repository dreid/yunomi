from snapshot import Snapshot
from random import randint


class UniformSample(object):
    BITS_PER_LONG = 63
    values = []

    def __init__(self, reservoirSize):
        self.values = [0 for x in xrange(reservoirSize)]
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
            r = UniformSample.nextLong(self.count)
            if r < len(self.values):
                self.values[r] = value

    @classmethod
    def nextLong(klass, n):
        return randint(0,n-1)

    def getSnapshot(self):
        return Snapshot(self.values)
