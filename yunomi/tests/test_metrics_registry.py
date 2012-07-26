from unittest2 import TestCase

from twisted.internet.task import Clock

from yunomi.core.metrics_registry import (MetricsRegistry, counter, histogram,
                                          meter, timer, count_calls,
                                          meter_calls, dist_calls, time_calls)


class MetricsRegistryTests(TestCase):

    def setUp(self):
        self.twisted_clock = Clock()
        self.registry = MetricsRegistry(clock=self.twisted_clock.seconds)

    def test_empty_registry(self):
        self.assertEqual(len(self.registry.dump_metrics()), 0)

    def test_getters_create_metrics(self):
        self.registry.counter("counter")
        self.registry.histogram("histogram")
        self.registry.meter("meter")
        self.registry.timer("timer")

        dump = self.registry.dump_metrics()

        self.assertEqual(len(dump), 25)
        metric_names = ("counter_count", "histogram_avg", "histogram_max",
                        "histogram_min", "histogram_std_dev",
                        "histogram_75_percentile", "histogram_98_percentile",
                        "histogram_99_percentile", "histogram_999_percentile",
                        "meter_15m_rate", "meter_5m_rate", "meter_1m_rate",
                        "meter_mean_rate", "timer_avg", "timer_max",
                        "timer_min", "timer_std_dev", "timer_75_percentile",
                        "timer_98_percentile", "timer_99_percentile",
                        "timer_999_percentile", "timer_15m_rate",
                        "timer_5m_rate", "timer_1m_rate", "timer_mean_rate")
        for stat in dump:
            self.assertTrue(stat["name"] in metric_names)
            self.assertEqual(stat["value"], 0)

    def test_count_calls_decorator(self):
        @count_calls
        def test():
            pass

        for i in xrange(10):
            test()
        self.assertEqual(counter("test_calls").get_count(), 10)

    def test_meter_calls_decorator(self):
        @meter_calls
        def test():
            pass

        for i in xrange(10):
            test()
            #some kind of timing thing here
        self.assertAlmostEqual(meter("test_calls").get_mean_rate(), 1.0)
