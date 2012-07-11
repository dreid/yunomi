from math import exp
from time import time
from random import random

from snapshot import Snapshot


class ExponentiallyDecayingSample(object):
    """
    An exponentially-decaying random sample of longs. Uses Cormode et al's
    forward-decaying priority reservoir sampling method to produce a
    statistically representative sample, exponentially biased towards newer
    entries.

    @see: <a href="http://www.research.att.com/people/Cormode_Graham/library/publications/CormodeShkapenyukSrivastavaXu09.pdf">
          Cormode et al. Forward Decay: A Practical Time Decay Model for
          Streaming Systems. ICDE '09: Proceedings of the 2009 IEEE
          International Conference on Data Engineering (2009)</a>
    """
    RESCALE_THRESHOLD = 3600
    count = 0
    values = {}
    next_scale_time = 0

    def __init__(self, reservoir_size, alpha, clock=time):
        """
        Creates a new L{ExponentiallyDecayingSample}.

        @type reservoir_size: C{int}
        @param reservoir_size: the number of samples to keep in the sampling
                               reservoir
        @type alpha: number
        @param alpha: the exponential decay factor; the higher this is, the more
                      biased the sample will be towards newer values
        @type clock: C{function}
        @param clock: the function used to return the current time, default to
                      seconds since the epoch; to be used with other time
                      units, or with the twisted clock for our testing purposes
        """
        self.reservoir_size = reservoir_size
        self.alpha = alpha
        self.clock = clock
        self.clear()

    def clear(self):
        """
        Clears the values in the sample and resets the clock.
        """
        self.count = 0
        self.values = {}
        self.start_time = self.clock()
        self.next_scale_time = self.clock() + self.RESCALE_THRESHOLD

    def size(self):
        """
        Returns the size of the exponentially decaying sample. The size does not
        increase if the I{count} exceeds the I{reservoir_size}. Instead, we
        wait until it is time for the sample rescale.

        @rtype: C{int}
        @return: the size of the sample
        """
        return min(self.reservoir_size, self.count)

    def update(self, value, timestamp=None):
        """
        Adds an old value with a fixed timestamp to the sample.

        @type value: C{int} or C{float}
        @param value: the value to be added
        @type timestamp: C{int}
        @param timestamp: the epoch timestamp of I{value} in seconds
        """
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
        """
        Checks the current time and rescales the sample if it time to do so.
        """
        now = self.clock()
        next_ = self.next_scale_time
        if now >= next_:
            self._rescale(now, next_)

    def get_snapshot(self):
        """
        Creates a statistical snapshot from the current set of values.
        """
        return Snapshot(self.values.values())

    def _weight(self, t):
        """
        Assigns a weight based on a specific timer interval, used to calculate
        priority for each value.
        """
        return exp(self.alpha * t)

    def _rescale(self, now, next_):
        """
        "A common feature of the above techniques—indeed, the key technique that
        allows us to track the decayed weights efficiently—is that they maintain
        counts and other quantities based on g(ti − L), and only scale by g(t − L)
        at query time. But while g(ti −L)/g(t−L) is guaranteed to lie between zero
        and one, the intermediate values of g(ti − L) could become very large. For
        polynomial functions, these values should not grow too large, and should be
        effectively represented in practice by floating point values without loss of
        precision. For exponential functions, these values could grow quite large as
        new values of (ti − L) become large, and potentially exceed the capacity of
        common floating point types. However, since the values stored by the
        algorithms are linear combinations of g values (scaled sums), they can be
        rescaled relative to a new landmark. That is, by the analysis of exponential
        decay in Section III-A, the choice of L does not affect the final result. We
        can therefore multiply each value based on L by a factor of exp(−α(L′ − L)),
        and obtain the correct value as if we had instead computed relative to a new
        landmark L′ (and then use this new L′ at query time). This can be done with
        a linear pass over whatever data structure is being used."
        """
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
