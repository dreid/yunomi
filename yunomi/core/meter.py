from time import time

from yunomi.stats.ewma import EWMA


class Meter(object):
    INTERVAL = 5

    _m1_rate = EWMA.one_minute_EWMA()
    _m5_rate = EWMA.five_minute_EWMA()
    _m15_rate = EWMA.fifteen_minute_EWMA()

    _count = 0

    def __init__(self, event_type, clock = time):
        self.event_type = event_type
        self.clock = clock
        self.start_time = self.clock()

    def get_event_type(self):
        return self.event_type

    def _tick(self):
        _m1_rate.tick()
        _m15_rate.tick()
        _m5_rate.tick()

    def mark(self, n = 1):
        self._count += n
        self._m1_rate.update(n)
        self._m15_rate.update(n)
        self._m5_rate.update(n)

    def get_count(self):
        return self._count

    def get_fifteen_minute_rate(self):
        return self._m15_rate.get_rate()

    def get_five_minute_rate(self):
        return self._m5_rate.get_rate()

    def get_one_minute_rate(self):
        return self._m1_rate.get_rate()

    def get_mean_rate(self):
        if self._count == 0:
            return 0.0
        else:
            elapsed = clock() - self.start_time
            return self._count / elapsed
