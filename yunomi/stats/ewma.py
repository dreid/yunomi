from math import exp
from time import time


class EWMA(object):
    """
    An exponentially-weighted moving average.

    @see: <a href="http://www.teamquest.com/pdfs/whitepaper/ldavg1.pdf">UNIX Load Average Part 1: How It Works</a>
    @see: <a href="http://www.teamquest.com/pdfs/whitepaper/ldavg2.pdf">UNIX Load Average Part 2: Not Your Average Average</a>
    """
    INTERVAL = 5

    def __init__(self, period, interval=None, clock = time):
        """
        Create a new EWMA with a specific smoothing constant.

        @type period: C{int}
        @param period: the time it takes to reach a given significance level
        @type interval: C{int}
        @param interval: the expected tick interval, defaults to 5s
        """
        self.initialized = False
        self._period = period
        self._interval = (interval or EWMA.INTERVAL)
        self._uncounted = 0.0
        self._rate = 0.0
        self.clock = clock
        self._last_tick = self.clock()

    @classmethod
    def one_minute_EWMA(klass, clock = time):
        """
        Creates a new EWMA which is equivalent to the UNIX one minute load
        average.

        @rtype: L{EWMA}
        @return: a one-minute EWMA
        """
        return klass(60, clock = clock)

    @classmethod
    def five_minute_EWMA(klass, clock = time):
        """
        Creates a new EWMA which is equivalent to the UNIX five minute load
        average.

        @rtype: L{EWMA}
        @return: a five-minute EWMA
        """
        return klass(300, clock = clock)

    @classmethod
    def fifteen_minute_EWMA(klass, clock = time):
        """
        Creates a new EWMA which is equivalent to the UNIX fifteen minute load
        average.

        @rtype: L{EWMA}
        @return: a fifteen-minute EWMA
        """
        return klass(900, clock = clock)

    def update(self, value):
        """
        Increment the moving average with a new value.

        @type value: C{int} or C{float}
        @param value: the new value
        """
        self._uncounted += value

    def tick(self):
        """
        Mark the passage of time and decay the current rate accordingly.
        """
        prev = self._last_tick
        now = self.clock()
        interval = now - prev

        instant_rate = self._uncounted / interval
        self._uncounted = 0.0

        if self.initialized:
            self._rate += (self._alpha(interval) * (instant_rate - self._rate))
        else:
            self._rate = instant_rate
            self.initialized = True

        self._last_tick = now

    def get_rate(self):
        """
        Returns the rate in counts per second. Calls L{EWMA.tick} when the
        elapsed time is greater than L{EWMA.INTERVAL}.

        @rtype: C{float}
        @return: the rate
        """
        if self.clock() - self._last_tick >= self._interval:
            self.tick()
        return self._rate

    def _alpha(self, interval):
        """
        Calculate the alpha based on the time since the last tick. This is
        necessary because a single threaded Python program loses precision  
        under high load, so we can't assume a consistant I{EWMA._interval}.

        @type interval: C{float}
        @param interval: the interval we use to calculate the alpha
        """
        return 1 - exp(-interval / self._period)
