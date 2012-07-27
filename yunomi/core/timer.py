from time import time

from yunomi.stats.snapshot import Snapshot
from yunomi.core.histogram import Histogram
from yunomi.core.meter import Meter


class Timer(object):
    """
    A timer metric which aggregates timing durations and provides duration
    statistics, plus throughput statistics via L{Meter}.
    """

    def __init__(self):
        """
        Creates a new L{Timer} instance.
        """
        self.histogram = Histogram.get_biased()
        self.meter = Meter("calls")

    def clear(self):
        """
        Clears all recorded durations in the histogram.
        """
        self.histogram.clear()

    def update(self, duration):
        """
        Updates the L{Histogram} and marks the L{Meter}.

        @type duration: C{int}
        @param duration: the duration of an event
        """
        if duration >= 0:
            self.histogram.update(duration)
            self.meter.mark()

    def get_count(self):
        """
        L{Histogram.get_count}
        """
        return self.histogram.get_count()

    def get_fifteen_minute_rate(self):
        """
        L{Meter.get_fifteen_minute_rate}
        """
        return self.meter.get_fifteen_minute_rate()

    def get_five_minute_rate(self):
        """
        L{Meter.get_five_minute_rate}
        """
        return self.meter.get_five_minute_rate()

    def get_one_minute_rate(self):
        """
        L{Meter.get_one_minute_rate}
        """
        return self.meter.get_one_minute_rate()

    def get_mean_rate(self):
        """
        L{Meter.get_mean_rate}
        """
        return self.meter.get_mean_rate()

    def get_max(self):
        """
        L{Histogram.get_max}
        """
        return self.histogram.get_max()

    def get_min(self):
        """
        L{Histogram.get_min}
        """
        return self.histogram.get_min()

    def get_mean(self):
        """
        L{Histogram.get_mean}
        """
        return self.histogram.get_mean()

    def get_std_dev(self):
        """
        L{Histogram.get_std_dev}
        """
        return self.histogram.get_std_dev()

    def get_sum(self):
        """
        L{Histogram.get_sum}
        """
        return self.histogram.get_sum()

    def get_snapshot(self):
        """
        L{Histogram.get_snapshot}
        """
        values = self.histogram.get_snapshot().get_values()
        return Snapshot(values)

    def get_event_type(self):
        """
        L{Meter.get_event_type}
        """
        return self.meter.get_event_type()
