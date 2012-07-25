from time import time

from yunomi.core.counter import Counter
from yunomi.core.histogram import Histogram
from yunomi.core.meter import Meter
from yunomi.core.timer import Timer


class MetricsRegistry(object):
    """
    A single interface used to gather metrics on a service. It keeps track of
    all the relevant Counters, Meters, Histograms, and Timers. It does not have
    a reference back to its service. The service would create a
    L{MetricsRegistry} to manage all of its metrics tools.
    """
    def __init__(self):
        """
        Creates a new L{MetricsRegistry} instance.

        @type clock: C{function}
        @param clock: the function used to return the current time, default to
                      seconds since the epoch; can be used with other time
                      units, or with the twisted clock for our testing purposes
        """
        self._timers = {}
        self._meters = {}
        self._counters = {}
        self._histograms = {}

    def get_counter(self, key):
        """
        Gets a counter based on a key, creates a new one if it does not exist.

        @param key: name of the metric
        @type key: C{str}

        @return: L{Counter}
        """
        if key not in self._counters:
            self._counters[key] = Counter()
        return self._counters[key]

    def get_histogram(self, key, biased=False):
        """
        Gets a histogram based on a key, creates a new one if it does not exist.

        @param key: name of the metric
        @type key: C{str}

        @return: L{Histogram}
        """
        if key not in self._histograms:
            if biased:
                self._histograms[key] = Histogram.get_biased()
            else:
                self._histograms[key] = Histogram.get_uniform()
                
        return self._histograms[key]

    def get_meter(self, key):
        """
        Gets a meter based on a key, creates a new one if it does not exist.

        @param key: name of the metric
        @type key: C{str}

        @return: L{Meter}
        """
        if key not in self._meters:
            self._meters[key] = Meter()
        return self._meters[key]

    def get_timer(self, key):
        """
        Gets a timer based on a key, creates a new one if it does not exist.

        @param key: name of the metric
        @type key: C{str}

        @return: L{Timer}
        """
        if key not in self._timers:
            self._timers[key] = Timer()
        return self._timers[key]

    def dump_metrics(self):
        """
        Formats all the metrics into dicts, and returns a list of all of them

        @return: C{list} of C{dict} of metrics
        """
        metrics = []

        # format timed stats
        for key, timer in self._timers.iteritems():
            snapshot = timer.get_snapshot()
            for suffix, val in (("avg", timer.get_mean()),
                                ("max", timer.get_max()),
                                ("min", timer.get_min()),
                                ("std_dev", timer.get_std_dev()),
                                ("15m_rate", timer.get_fifteen_minute_rate()),
                                ("5m_rate", timer.get_five_minute_rate()),
                                ("1m_rate", timer.get_one_minute_rate()),
                                ("mean_rate", timer.get_mean_rate()),
                                ("75_percentile", snapshot.get_75th_percentile()),
                                ("98_percentile", snapshot.get_98th_percentile()),
                                ("99_percentile", snapshot.get_99th_percentile()),
                                ("999_percentile", snapshot.get_999th_percentile())):
                k = "_".join([key, suffix])
                _new_metric = {
                    "type": "float",
                    "name": k,
                    "value": val,
                }
                metrics.append(_new_metric)

        # format meter stats
        for key, meter in self._meters.iteritems():
            for suffix, val in (("15m_rate", meter.get_fifteen_minute_rate()),
                                ("5m_rate", meter.get_five_minute_rate()),
                                ("1m_rate", meter.get_one_minute_rate()),
                                ("mean_rate", meter.get_mean_rate())):
                k = "_".join([key, suffix])
                _new_metric = {
                    "type": "float",
                    "name": k,
                    "value": val,
                }
                metrics.append(_new_metric)

        # format histogram stats
        for key, histogram in self._histograms.iteritems():
            snapshot = histogram.get_snapshot()
            for suffix, val in (("avg", histogram.get_mean()),
                                ("max", histogram.get_max()),
                                ("min", histogram.get_min()),
                                ("std_dev", histogram.get_std_dev()),
                                ("75_percentile", snapshot.get_75th_percentile()),
                                ("98_percentile", snapshot.get_98th_percentile()),
                                ("99_percentile", snapshot.get_99th_percentile()),
                                ("999_percentile", snapshot.get_999th_percentile())):
                k = "_".join([key, suffix])
                _new_metric = {
                    "type": "float",
                    "name": k,
                    "value": val,
                }
                metrics.append(_new_metric)

        # format counter stats
        for key, counter in self._counters.iteritems():
            k = "_".join([key, "count"])
            val = counter.get_count()
            _new_metric = {
                "type": "int",
                "name": k,
                "value": val
            }
            metrics.append(_new_metric)

        # alphabetize
        metrics.sort(key=lambda x: x["name"])
        return metrics


_global_registry= MetricsRegistry()

counter = _global_registry.get_counter
histogram = _global_registry.get_histogram
meter = _global_registry.get_meter
timer = _global_registry.get_timer
dump_metrics = _global_registry.dump_metrics
