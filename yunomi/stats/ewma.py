from math import exp


class EWMA(object):
    """
    An exponentially-weighted moving average.

    @see: <a href="http://www.teamquest.com/pdfs/whitepaper/ldavg1.pdf">UNIX Load Average Part 1: How It Works</a>
    @see: <a href="http://www.teamquest.com/pdfs/whitepaper/ldavg2.pdf">UNIX Load Average Part 2: Not Your Average Average</a>
    """
    INTERVAL = 5
    SECONDS_PER_MINUTE = 60.0
    ONE_MINUTE = 1
    FIVE_MINUTES = 5
    FIFTEEN_MINUTES = 15
    M1_ALPHA = 1 - exp(-INTERVAL / SECONDS_PER_MINUTE / ONE_MINUTE)
    M5_ALPHA = 1 - exp(-INTERVAL / SECONDS_PER_MINUTE / FIVE_MINUTES)
    M15_ALPHA = 1 - exp(-INTERVAL / SECONDS_PER_MINUTE / FIFTEEN_MINUTES)

    def __init__(self, alpha, interval=None):
        """
        Create a new EWMA with a specific smoothing constant.

        @type         alpha: number
        @param        alpha: the smoothing constant
        @param     interval: the expected tick interval
        @param intervalUnit: the time unit of the tick interval
        """
        self.initialized = False
        self._alpha = alpha
        self._interval = (interval or EWMA.INTERVAL)
        self._uncounted = 0.0
        self._rate = 0.0

    @classmethod
    def one_minute_EWMA(klass):
        """
        Creates a new EWMA which is equivalent to the UNIX one minute load average and which expects
        to be ticked every 5 seconds.

        @rtype:  EWMA
        @return: a one-minute EWMA
        """
        return klass(klass.M1_ALPHA)

    @classmethod
    def five_minute_EWMA(klass):
        """
        Creates a new EWMA which is equivalent to the UNIX five minute load average and which expects
        to be ticked every 5 seconds.

        @rtype:  EWMA
        @return: a one-minute EWMA
        """
        return klass(klass.M5_ALPHA)

    @classmethod
    def fifteen_minute_EWMA(klass):
        """
        Creates a new EWMA which is equivalent to the UNIX fifteen minute load average and which expects
        to be ticked every 5 seconds.

        @rtype:  EWMA
        @return: a one-minute EWMA
        """
        return klass(klass.M15_ALPHA)

    def update(self, value):
        """
        Increment the moving average with a new value.

        @type  value: number
        @param value: the new value
        """
        self._uncounted += value

    def tick(self):
        """
        Mark the passage of time and decay the current rate accordingly.
        """
        instantRate = self._uncounted / self._interval
        self._uncounted = 0.0

        if self.initialized:
            self._rate += (self._alpha * (instantRate - self._rate))
        else:
            self._rate = instantRate
            self.initialized = True

    def get_rate(self):
        """
        Returns the rate in counts per second.

        @rtype:  number
        @return: the rate
        """
        return self._rate
