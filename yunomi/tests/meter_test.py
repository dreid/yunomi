from unittest import TestCase

from yunomi.core.meter import Meter


class MeterTests(TestCase):
    _meter = Meter("things")

    def test_a_blank_meter(self):
        self.assertEqual(self._meter.get_count(), 0)
        self.assertAlmostEqual(self._meter.get_mean_rate(), 0.0)

    def test_a_meter_with_three_events(self):
        self._meter.mark(3)
        self.assertEqual(self._meter.get_count(), 3)
