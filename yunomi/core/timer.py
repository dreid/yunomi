from time import time

from yunomi.stats.snapshot import Snapshot
from yunomi.core.histogram import Histogram
from yunomi.core.meter import Meter


class Timer(object):
    histogram = Histogram(Histogram.SampleType.BIASED)

    def __init__(self, clock = time):
        self.clock = clock
        self.meter = Meter("calls", self.clock)

    def clear(self):
        self.histogram.clear()

    def clear(self):
        self.histogram.clear()

    def update(self, duration):
        if duration >= 0:
            self.histogram.update(duration)
            self.meter.mark()

    def time(self):
        return self.clock()

    def get_count(self):
        return self.histogram.get_count()

    def get_fifteen_minute_rate(self):
        return self.meter.get_fifteen_minute_rate()

    def get_five_minute_rate(self):
        return self.meter.get_five_minute_rate()

    def get_one_minute_rate(self):
        return self.meter.get_one_minute_rate()

    def get_mean_rate(self):
        return self.meter.get_mean_rate()

    def get_max(self):
        return self.histogram.get_max()

    def get_min(self):
        return self.histogram.get_min()

    def get_mean(self):
        return self.histogram.get_mean()

    def get_std_dev(self):
        return self.histogram.get_std_dev()

    def get_sum(self):
        return self.histogram.get_sum()

    def get_snapshot(self):
        values = self.histogram.get_snapshot().get_values()
        return Snapshot(values)

    def get_event_type(self):
        return self.meter.get_event_type()

    def stop(self):
        meter.stop()
