from time import time

from yunomi.stats.ewma import EWMA


class Meter(object):
    """
    A meter metric which measures mean throughput and one-, five-, and fifteen-
    minute exponentially-weighted moving average throughputs.

    @see: <a href="http://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average">EMA</a>
    """
    INTERVAL = 5

    def __init__(self, event_type, clock = time):
        """
        Creates a new L{Meter} instance.

        @type event_type: C{str}
        @param event_type: the plural name of the event the meter is measuring
                           (e.g., I{"requests"})
        @type clock: C{function}
        @param clock: the function used to return the current time, default to
                      seconds since the epoch; to be used with other time
                      units, or with the twisted clock for our testing purposes
        """
        self.event_type = event_type
        self.clock = clock
        self.start_time = self.clock()
        self._m1_rate = EWMA.one_minute_EWMA()
        self._m5_rate = EWMA.five_minute_EWMA()
        self._m15_rate = EWMA.fifteen_minute_EWMA()
        self._count = 0

    def get_event_type(self):
        """
        Returns the event type.

        @rtype: C{str}
        @return: the event type
        """
        return self.event_type

    def _tick(self):
        """
        Updates the moving averages.
        """
        self._m1_rate.tick()
        self._m15_rate.tick()
        self._m5_rate.tick()

    def mark(self, n = 1):
        """
        Mark the occurrence of a given number of events.

        @type n: C{int}
        @param n: number of events
        """
        self._count += n
        self._m1_rate.update(n)
        self._m15_rate.update(n)
        self._m5_rate.update(n)

    def get_count(self):
        """
        Return the number of events that have been counted.

        @rtype: C{int}
        @return: the total number of events
        """
        return self._count

    def get_fifteen_minute_rate(self):
        """
        Get the rate of the L{EWMA} equivalent to a fifteen minute load average.

        @rtype: C{float}
        @return: the fifteen minute rate
        """
        return self._m15_rate.get_rate()

    def get_five_minute_rate(self):
        """
        Get the rate of the L{EWMA} equivalent to a five minute load average.

        @rtype: C{float}
        @return: the five minute rate
        """
        return self._m5_rate.get_rate()

    def get_one_minute_rate(self):
        """
        Get the rate of the L{EWMA} equivalent to a one minute load average.

        @rtype: C{float}
        @return: the one minute rate
        """
        return self._m1_rate.get_rate()

    def get_mean_rate(self):
        """
        Get the overall rate, the total number of events over the time since
        the beginning.

        @rtype: C{float}
        @return: the mean minute rate
        """
        if self._count == 0:
            return 0.0
        else:
            elapsed = self.clock() - self.start_time
            return float(self._count) / elapsed
