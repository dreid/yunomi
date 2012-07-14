from unittest import TestCase

from twisted.internet.task import Clock

from yunomi.stats.ewma import EWMA


class EWMATests(TestCase):

    def elapse_minute(self, ewma, twisted_clock):
        for i in xrange(0, 12):
            twisted_clock.advance(5)
            ewma.tick()

    def test_one_minute_EWMA_five_sec_tick(self):
        twisted_clock = Clock()
        ewma = EWMA.one_minute_EWMA(clock = twisted_clock.seconds)

        ewma.update(3)
        twisted_clock.advance(5)
        ewma.tick()

        for expected_rate in [0.6, 0.22072766, 0.08120117, 0.02987224,
                              0.01098938, 0.00404277, 0.00148725,
                              0.00054713, 0.00020128, 0.00007405]:
            self.assertAlmostEqual(ewma.get_rate(), expected_rate)
            self.elapse_minute(ewma, twisted_clock)

    def test_five_minute_EWMA_five_sec_tick(self):
        twisted_clock = Clock()
        ewma = EWMA.five_minute_EWMA(clock = twisted_clock.seconds)

        ewma.update(3)
        twisted_clock.advance(5)
        ewma.tick()

        for expected_rate in [0.6, 0.49123845, 0.40219203, 0.32928698,
                              0.26959738, 0.22072766, 0.18071653,
                              0.14795818, 0.12113791, 0.09917933]:
            self.assertAlmostEqual(ewma.get_rate(), expected_rate)
            self.elapse_minute(ewma, twisted_clock)

    def test_fifteen_minute_EWMA_five_sec_tick(self):
        twisted_clock = Clock()
        ewma = EWMA.fifteen_minute_EWMA(clock = twisted_clock.seconds)

        ewma.update(3)
        twisted_clock.advance(5)
        ewma.tick()

        for expected_rate in [0.6, 0.56130419, 0.52510399, 0.49123845,
                              0.45955700, 0.42991879, 0.40219203,
                              0.37625345, 0.35198773, 0.32928698]:
            self.assertAlmostEqual(ewma.get_rate(), expected_rate)
            self.elapse_minute(ewma, twisted_clock)

    def test_one_minute_EWMA_one_minute_tick(self):
        twisted_clock = Clock()
        ewma = EWMA.one_minute_EWMA(clock = twisted_clock.seconds)

        ewma.update(3)
        twisted_clock.advance(5)
        ewma.tick()

        for expected_rate in [0.6, 0.22072766, 0.08120117, 0.02987224,
                              0.01098938, 0.00404277, 0.00148725,
                              0.00054713, 0.00020128, 0.00007405]:
            self.assertAlmostEqual(ewma.get_rate(), expected_rate)
            twisted_clock.advance(60)

    def test_five_minute_EWMA_one_minute_tick(self):
        twisted_clock = Clock()
        ewma = EWMA.five_minute_EWMA(clock = twisted_clock.seconds)

        ewma.update(3)
        twisted_clock.advance(5)
        ewma.tick()

        for expected_rate in [0.6, 0.49123845, 0.40219203, 0.32928698,
                              0.26959738, 0.22072766, 0.18071653,
                              0.14795818, 0.12113791, 0.09917933]:
            self.assertAlmostEqual(ewma.get_rate(), expected_rate)
            twisted_clock.advance(60)

    def test_fifteen_minute_EWMA_one_minute_tick(self):
        twisted_clock = Clock()
        ewma = EWMA.fifteen_minute_EWMA(clock = twisted_clock.seconds)

        ewma.update(3)
        twisted_clock.advance(5)
        ewma.tick()

        for expected_rate in [0.6, 0.56130419, 0.52510399, 0.49123845,
                              0.45955700, 0.42991879, 0.40219203,
                              0.37625345, 0.35198773, 0.32928698]:
            self.assertAlmostEqual(ewma.get_rate(), expected_rate)
            twisted_clock.advance(60)
