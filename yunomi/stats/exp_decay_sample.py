from math import exp
from time import time
from random import random

from snapshot import Snapshot


class ExponentiallyDecayingSample(object):
    RESCALE_THRESHOLD = 3600
    count = 0
    values = {}
    next_scale_time = 0

    def __init__(self, reservoir_size, alpha, clock=time):
        self.reservoir_size = reservoir_size
        self.alpha = alpha
        self.clock = clock
        self.clear()

    def clear(self):
        self.count = 0
        self.values = {}
        self.start_time = self.clock()
        self.next_scale_time = self.clock() + self.RESCALE_THRESHOLD

    def size(self):
        return min(self.reservoir_size, self.count)

    def update(self, value, timestamp=None):
        if not timestamp:
            timestamp = self.clock()
        self._rescale_if_needed()
        priority = self._weight(timestamp - self.start_time) / random()
        self.count += 1

        if self.count <= self.reservoir_size:
            self.values[priority] = value
        else:
            first = min(self.values)
            if first < priority:
                if priority not in self.values:
                    self.values[priority] = value
                    while first not in self.values:
                        first = min(self.values)
                    del self.values[first]

    def _rescale_if_needed(self):
        now = self.clock()
        next_ = self.next_scale_time
        if now >= next_:
            self._rescale(now, next_)

    def get_snapshot(self):
        return Snapshot(self.values.values())

    def _weight(self, t):
        return exp(self.alpha * t)

    def _rescale(self, now, next_):
        if self.next_scale_time == next_:
            self.next_scale_time = now + self.RESCALE_THRESHOLD
            old_start_time = self.start_time
            self.start_time = self.clock()
            keys = self.values.keys()
            keys.sort()

            for key in keys:
                value = self.values[key]
                del self.values[key]
                self.values[key * exp(-self.alpha * (self.start_time - old_start_time))] = value

            self.count = len(self.values)
