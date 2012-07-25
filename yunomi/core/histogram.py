from math import sqrt

from yunomi.stats.exp_decay_sample import ExponentiallyDecayingSample
from yunomi.stats.uniform_sample import UniformSample


class Histogram(object):
    """
    A metric which calculates the distribution of a value.

    @see: <a href="http://www.johndcook.com/standard_deviation.html">Accurately computing running variance</a>
    """
    DEFAULT_SAMPLE_SIZE = 1028
    DEFAULT_ALPHA = 0.015
    count = 0
    mean = 0
    sum_of_squares = -1.0

    def __init__(self, sample):
        """
        Creates a new instance of a L{Histogram}.

        @type sample: L{ExponentiallyDecayingSample} or L{UniformSample}
        @param sample: an instance of L{ExponentiallyDecayingSample} or
                       L{UniformSample}
        """
        self.sample = sample
        self.clear()

    @classmethod
    def get_biased(klass):
        """
        Create a new instance of L{Histogram} that uses an L{ExponentiallyDecayingSample}
        with sample size L{DEFAULT_SAMPLE_SIZE} and alpha L{DEFAULT_ALPHA}.

        @return: L{Histogram}
        """
        return klass(ExponentiallyDecayingSample(klass.DEFAULT_SAMPLE_SIZE, klass.DEFAULT_ALPHA))

    @classmethod
    def get_uniform(klass):
        """
        Create a new instance of L{Histogram} that uses an L{UniformSample}
        with sample size L{DEFAULT_SAMPLE_SIZE}.

        """
        return klass(UniformSample(klass.DEFAULT_SAMPLE_SIZE))

    def clear(self):
        """
        Resets the values to default.
        """
        self.sample.clear()
        self.max_ = -2147483647.0
        self.min_ = 2147483647.0
        self.sum_ = 0.0
        self.count = 0
        self.mean = 0
        self.sum_of_squares = -1.0

    def update(self, value):
        """
        Updates all the fields with the new value (if applicable).

        @type value: C{int}
        @param value: the value to update the fields with
        """
        self.count += 1
        self.sample.update(value)
        self.set_max(value)
        self.set_min(value)
        self.sum_ += value
        self.update_variance_info(value)

    def get_count(self):
        """
        The number of values put into the histogram.
        """
        return self.count

    def get_max(self):
        """
        The maximum value that has been updated into the histogram.

        @rtype: C{int} or C{float}
        @return: the max value
        """
        if self.get_count() > 0:
            return self.max_
        return 0.0

    def get_min(self):
        """
        The minimum value that has been updated into the histogram.

        @rtype: C{int} or C{float}
        @return: the min value
        """
        if self.get_count() > 0:
            return self.min_
        return 0.0

    def get_mean(self):
        """
        The average of all the values that have been updated into the
        historgram.

        @rtype: C{float}
        @return: the average of all the values updated
        """
        if self.get_count() > 0:
            return float(self.sum_) / self.get_count()
        return 0.0

    def get_std_dev(self):
        """
        Returns the standard devation calculated by taking the square root of
        the variance, which is updated whenever a new value is added.

        @rtype: C{float}
        @return: the standard deviation
        """
        if self.get_count() > 0:
            return sqrt(self.get_variance())
        return 0.0

    def get_variance(self):
        """
        Returns the variance calculated using the sum of squares of deviations
        from the mean and the total count, which are both updated whenever a
        new value is added.

        @rtype: C{float}
        @return: the variance
        """
        if self.get_count() <= 1:
            return 0.0
        return self.sum_of_squares / (self.get_count() - 1)

    def get_sum(self):
        """
        The sum of all the values, updated whenever a value is added. Useful
        for computing the mean quickly.

        @rtype: C{int} or C{float}
        @return: the sum of all the values
        """
        return self.sum_

    def get_snapshot(self):
        """
        Returns a snapshot of the current set of values in the histogram.

        @rtype: L{Snapshot}
        @return: the snapshot of the current values
        """
        return self.sample.get_snapshot()

    def set_max(self, new_max):
        """
        Checks if a value is greater than the current max. If so, update
        I{max_}.

        @type new_max: C{int} or C{float}
        @param new_max: the potential new maximum value to check
        """
        if self.max_ < new_max:
            self.max_ = new_max

    def set_min(self, new_min):
        """
        Checks if a value is less than the current min. If so, update I{min_}.

        @type new_min: C{int} or C{float}
        @param new_min: the potential new minimum value to check
        """
        if self.min_ > new_min:
            self.min_ = new_min

    def update_variance_info(self, value):
        """
        Updates the I{sum_of_squares} and I{mean} whenever a new value is
        updated. This makes computing the variance more computationally
        efficient.

        @type value: C{int} or C{float}
        @param value: the value being added to the histogram
        """
        old_mean = self.mean
        delta = value - old_mean
        if self.sum_of_squares == -1.0:
            self.mean = value
            self.sum_of_squares = 0.0
        else:
            self.mean += (float(delta) / self.get_count())
            self.sum_of_squares += (float(delta) * (value - self.mean))
