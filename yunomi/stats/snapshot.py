from math import floor


class Snapshot(object):
    MEDIAN_Q = 0.5
    P75_Q = 0.75
    P95_Q = 0.95
    P98_Q = .98
    P99_Q = .99
    P999_Q = .999

    def __init__(self, values):
        self.values = values[:]
        self.values.sort()

    def get_value(self, quantile):
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
        return len(self.values)

    def get_median(self):
        return self.get_value(self.MEDIAN_Q)

    def get_75th_percentile(self):
        return self.get_value(self.P75_Q)

    def get_98th_percentile(self):
        return self.get_value(self.P98_Q)

    def get_99th_percentile(self):
        return self.get_value(self.P99_Q)

    def get_999th_percentile(self):
        return self.get_value(self.P999_Q)

    def get_values(self):
        return self.values[:]

    def dump(output):
        assert type(output) == file, "Argument must be of 'file' type"

        for value in self.values:
            output.write("{0}\n".format(value))
        output.close()
