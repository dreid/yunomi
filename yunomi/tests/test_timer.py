from unittest import TestCase

from twisted.internet.task import Clock

from yunomi.core.timer import Timer
from yunomi.stats.snapshot import Snapshot


class TimerTests(TestCase):

    def setUp(self):
        self.timer = Timer(Clock().seconds)

    def test_blank_timer(self):
        self.assertEqual(self.timer.get_count(), 0)
        self.assertAlmostEqual(self.timer.get_max(), 0.0)
        self.assertAlmostEqual(self.timer.get_min(), 0.0)
        self.assertAlmostEqual(self.timer.get_mean(), 0.0)
        self.assertAlmostEqual(self.timer.get_std_dev(), 0.0)

        snapshot = self.timer.get_snapshot()
        self.assertAlmostEqual(snapshot.get_median(), 0.0)
        self.assertAlmostEqual(snapshot.get_75th_percentile(), 0.0)
        self.assertAlmostEqual(snapshot.get_99th_percentile(), 0.0)
        self.assertEqual(self.timer.get_snapshot().size(), 0)

        self.assertAlmostEqual(self.timer.get_mean_rate(), 0.0)
        self.assertAlmostEqual(self.timer.get_one_minute_rate(), 0.0)
        self.assertAlmostEqual(self.timer.get_five_minute_rate(), 0.0)
        self.assertAlmostEqual(self.timer.get_fifteen_minute_rate(), 0.0)

    def test_timing_a_series_of_events(self):
        self.timer = Timer()
        self.timer.update(10)
        self.timer.update(20)
        self.timer.update(20)
        self.timer.update(30)
        self.timer.update(40)

        self.assertEqual(self.timer.get_count(), 5)
        self.assertAlmostEqual(self.timer.get_max(), 40.0)
        self.assertAlmostEqual(self.timer.get_min(), 10.0)
        self.assertAlmostEqual(self.timer.get_mean(), 24.0)
        self.assertAlmostEqual(self.timer.get_std_dev(), 11.401, places=2)

        snapshot = self.timer.get_snapshot()
        self.assertAlmostEqual(snapshot.get_median(), 20.0)
        self.assertAlmostEqual(snapshot.get_75th_percentile(), 35.0)
        self.assertAlmostEqual(snapshot.get_99th_percentile(), 40.0)
        self.assertEqual(self.timer.get_snapshot().get_values(),
                         [10.0, 20.0, 20.0, 30.0, 40.0])

    def test_timing_variant_values(self):
        self.timer.clear()
        self.timer.update(9223372036854775807)
        self.timer.update(0)
        self.assertAlmostEqual(self.timer.get_std_dev(), 6521908912666392000)
