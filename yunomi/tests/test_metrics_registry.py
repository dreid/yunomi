from unittest2 import TestCase

from yunomi.core.metrics_registry import MetricsRegistry


class MetricsRegistryTests(TestCase):

    def setUp(self):
        self.registry = MetricsRegistry()

    def test_empty_registry(self):
        self.assertEqual(len(self.registry.dump_metrics()), 0)

    def test_getters_create_metrics(self):
        self.registry.get_counter("counter")
        self.registry.get_histogram("histogram")
        self.registry.get_meter("meter")
        self.registry.get_timer("timer")

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
