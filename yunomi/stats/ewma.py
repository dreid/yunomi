from math import exp


class EWMA(object):
    INTERVAL = 5
    SECONDS_PER_MINUTE = 60.0
    ONE_MINUTE = 1
    FIVE_MINUTES = 5
    FIFTEEN_MINUTES = 15
    M1_ALPHA = 1 - exp(-INTERVAL / SECONDS_PER_MINUTE / ONE_MINUTE)
    M5_ALPHA = 1 - exp(-INTERVAL / SECONDS_PER_MINUTE / FIVE_MINUTES)
    M15_ALPHA = 1 - exp(-INTERVAL / SECONDS_PER_MINUTE / FIFTEEN_MINUTES)

    def __init__(self, alpha, interval=None):
        self._alpha = alpha
        self._interval = (interval or EWMA.INTERVAL) * 1000000000
        self._uncounted = 0.0
        self._rate = None

    @classmethod
    def one_minute_EWMA(klass):
        return klass(klass.M1_ALPHA)

    @classmethod
    def five_minute_EWMA(klass):
        return klass(klass.M5_ALPHA)

    @classmethod
    def fifteen_minute_EWMA(klass):
        return klass(klass.M15_ALPHA)

    def update(self, value):
        self._uncounted += value

    def tick(self):
        count = self._uncounted
        self._uncounted = 0.0

        instantRate = count / self._interval

        if self._rate:
            self._rate += (self._alpha * (instantRate - self._rate))
        else:
            self._rate = instantRate

    def get_rate(self):
        return self._rate * 1000000000
