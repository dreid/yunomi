from __future__ import division, absolute_import

import mock
from unittest2 import TestCase

from yunomi.compat import xrange
from yunomi.core.meter import Meter


class MeterTests(TestCase):

    def test_a_blankmeter(self):
        self.meter = Meter("test")
        self.assertEqual(self.meter.get_count(), 0)
        self.assertAlmostEqual(self.meter.get_mean_rate(), 0.0)

    def test_meter_with_three_events(self):
        self.meter = Meter("test")
        self.meter.mark(3)
        self.assertEqual(self.meter.get_count(), 3)

    @mock.patch("yunomi.core.meter.time")
    def test_mean_rate_one_per_second(self, time_mock):
        time_mock.return_value = 0.0
        self.meter = Meter("test")
        for i in xrange(10):
            self.meter.mark()
            time_mock.return_value += 1

        self.meter._tick()
        self.assertAlmostEqual(self.meter.get_mean_rate(), 1)

    @mock.patch("yunomi.stats.ewma.time")
    def test_meter_EWMA_rates(self, time_mock):
        time_mock.return_value = 0.0
        self.meter = Meter("test")
        self.meter.mark(3)
        time_mock.return_value += 5

        for one, five, fifteen in [(0.6, 0.6, 0.6),
                                   (0.22072766, 0.49123845, 0.56130419),
                                   (0.08120117, 0.40219203, 0.52510399),
                                   (0.02987224, 0.32928698, 0.49123845),
                                   (0.01098938, 0.26959738, 0.45955700),
                                   (0.00404277, 0.22072766, 0.42991879),
                                   (0.00148725, 0.18071653, 0.40219203),
                                   (0.00054713, 0.14795818, 0.37625345),
                                   (0.00020128, 0.12113791, 0.35198773),
                                   (0.00007405, 0.09917933, 0.32928698)]:
            self.assertAlmostEqual(self.meter.get_one_minute_rate(), one)
            self.assertAlmostEqual(self.meter.get_five_minute_rate(), five)
            self.assertAlmostEqual(self.meter.get_fifteen_minute_rate(), fifteen)
            time_mock.return_value += 60
