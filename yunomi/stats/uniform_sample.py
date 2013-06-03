from __future__ import division, absolute_import

from random import randint

from yunomi.compat import xrange
from yunomi.stats.snapshot import Snapshot


class UniformSample(object):
    """
    A random sample of a stream of {@code long}s. Uses Vitter's Algorithm R to
    produce a statistically representative sample.

    @see: <a href="http://www.cs.umd.edu/~samir/498/vitter.pdf">Random Sampling with a Reservoir</a>
    """
    BITS_PER_LONG = 63
    values = []

    def __init__(self, reservoir_size):
        """
        Create a new L{UniformSample}.

        @type reservoir_size: C{int}
        @param reservoir_size: the number of params to keep in the sampling reservoir
        """
        self.values = [0 for x in xrange(reservoir_size)]
        self.clear()

    def clear(self):
        """
        Clears the sample, setting all values to zero.
        """
        self.values = [0 for x in xrange(len(self.values))]
        self.count = 0

    def size(self):
        """
        Returns the size of the uniform sample. The size will never be bigger
        than the reservoir_size (ie. the size of the list of values).

        @rtype: C{int}
        @return: the size of the sample
        """
        
        if self.count > len(self.values):
            return len(self.values)
        return self.count

    def update(self, value):
        """
        Updates the I{self.values} at a random index with the given value.

        @type value: C{int} or C{float}
        @param value: the new value to be added
        """
        self.count += 1
        if self.count <= len(self.values):
            self.values[self.count - 1] = value
        else:
            r = UniformSample.next_long(self.count)
            if r < len(self.values):
                self.values[r] = value

    @classmethod
    def next_long(klass, n):
        """
        Randomly assigns a new number in [0...n]. Used to randomly update an
        index in I{self.values} with a new value.
        """
        return randint(0, n-1)

    def get_snapshot(self):
        """
        Creates a statistical snapshot from the current set of values.
        """
        copy = []
        for i in xrange(self.size()):
            copy.append(self.values[i])
        return Snapshot(copy)
