from unittest import TestCase

from yunomi.core.meter import Meter


class MeterTests(TestCase):
    def setUp(self):
        self.meter = Meter("test")

    def test_a_blankmeter(self):
        self.assertEqual(self.meter.get_count(), 0)
        self.assertAlmostEqual(self.meter.get_mean_rate(), 0.0)

    def test_ameter_with_three_events(self):
        self.meter.mark(3)
        self.assertEqual(self.meter.get_count(), 3)
