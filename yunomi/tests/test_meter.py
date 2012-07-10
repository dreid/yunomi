from unittest import TestCase

from twisted.internet.task import Clock

from yunomi.core.meter import Meter


class MeterTests(TestCase):
    def setUp(self):
        self.meter = Meter("test")

    def test_a_blankmeter(self):
        self.assertEqual(self.meter.get_count(), 0)
        self.assertAlmostEqual(self.meter.get_mean_rate(), 0.0)

    def test_meter_with_three_events(self):
        self.meter.mark(3)
        self.assertEqual(self.meter.get_count(), 3)

    def test_meter_rate_one_per_second(self):
        twisted_clock = Clock()
        self.meter = Meter("test", twisted_clock.seconds)

        for i in xrange(100):
            self.meter.mark()
            twisted_clock.advance(1)

        self.meter._tick()
        self.assertAlmostEqual(self.meter.get_mean_rate(), 1)
