from math import floor


class Snapshot(object):
    """
    A statistical snapshot of a set of values.
    """
    MEDIAN_Q = 0.5
    P75_Q = 0.75
    P95_Q = 0.95
    P98_Q = .98
    P99_Q = .99
    P999_Q = .999

    def __init__(self, values):
        """
        Create a new L{Snapshot} with the given values.

        @type values: C{dict}
        @param values: an unordered set of values in the sample
        """
        self.values = values[:]
        self.values.sort()

    def get_value(self, quantile):
        """
        Returns the value at the given quantile.

        @type quantile: C{float}
        @param quantile: a given quantile in M{[0...1]}

        @rtype: C{int} or C{float}
        @return: the value in the distribution at the specified I{quantile}
        """
        assert quantile >= 0.0 and quantile <= 1.0,\
            "{0} is not in [0...1]".format(quantile)
        if len(self.values) == 0:
            return 0.0

        pos = quantile * (len(self.values) + 1)

        if pos < 1:
            return self.values[0]
        if pos >= len(self.values):
            return self.values[len(self.values) -1]

        lower = self.values[int(pos) - 1]
        upper = self.values[int(pos)]
        return lower + (pos - floor(pos)) * (upper - lower)

    def size(self):
        """
        Return the size of the given distribution.

        @rtype: C{int}
        @return: the size of the given distribution
        """
        return len(self.values)

    def get_median(self):
        """
        Return the median of the given distribution.

        @rtype: C{int}
        @return: the median
        """
        return self.get_value(self.MEDIAN_Q)

    def get_75th_percentile(self):
        """
        Return the 75th percentile value of the given distribution.

        @rtype: C{int}
        @return: the 99.9th percentile value
        """
        return self.get_value(self.P75_Q)

    def get_98th_percentile(self):
        """
        Return the 98th percentile value of the given distribution.

        @rtype: C{int}
        @return: the 98th percentile value
        """
        return self.get_value(self.P98_Q)

    def get_99th_percentile(self):
        """
        Return the 99th percentile value of the given distribution.

        @rtype: C{int}
        @return: the 99th percentile value
        """
        return self.get_value(self.P99_Q)

    def get_999th_percentile(self):
        """
        Return the 99.9th percentile value of the given distribution.

        @rtype: C{int}
        @return: the 99.9th percentile value
        """
        return self.get_value(self.P999_Q)

    def get_values(self):
        """
        Returns a copy of the current distribution of values

        @rtype: C{list}
        @return: a copy of the list of values
        """
        return self.values[:]

    def dump(output):
        """
        Write all the values to a file

        @todo: actually test this to see if it works...
        """
        assert type(output) == file, "Argument must be of 'file' type"

        for value in self.values:
            output.write("{0}\n".format(value))
        output.close()
