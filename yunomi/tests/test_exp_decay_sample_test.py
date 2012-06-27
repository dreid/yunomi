from unittest import TestCase

from twisted.internet.task import Clock

from yunomi.stats.exp_decay_sample import ExponentiallyDecayingSample
from yunomi.stats.snapshot import Snapshot


class ExponentiallyDecayingSampleTests(TestCase):

    def test_a_sample_of_100_out_of_1000_elements(self):
        sample = ExponentiallyDecayingSample(100, 0.99)
        for i in xrange(1000):
            sample.update(i)
        snapshot = sample.get_snapshot()

        self.assertEqual(sample.size(), 100)
        self.assertEqual(snapshot.size(), 100)

        for i in snapshot.get_values():
            self.assertTrue(i < 1000 and i >= 0)

    def test_a_sample_of_100_out_of_10_elements(self):
        sample = ExponentiallyDecayingSample(100, 0.99)
        for i in xrange(10):
            sample.update(i)
        snapshot = sample.get_snapshot()

        self.assertEqual(sample.size(), 10)
        self.assertEqual(snapshot.size(), 10)
        self.assertAlmostEqual(snapshot.get_median(), 4.5)

        for i in snapshot.get_values():
            self.assertTrue(i < 10 and i >= 0)

    def test_a_heavily_biased_sample_of_100_out_of_1000_elements(self):
        sample = ExponentiallyDecayingSample(1000, 0.01)
        for i in xrange(100):
            sample.update(i)
        snapshot = sample.get_snapshot()

        self.assertEqual(sample.size(), 100)
        self.assertEqual(snapshot.size(), 100)

        for i in snapshot.get_values():
            self.assertTrue(i < 100 and i >= 0)

    def test_long_period_of_inactivity_should_not_corrupt_sampling_state(self):
        twisted_clock = Clock()
        sample = ExponentiallyDecayingSample(10, 0.015, twisted_clock.seconds)
        for i in xrange(1000):
            sample.update(1000 + i)
            twisted_clock.advance(0.1)

        self.assertTrue(sample.get_snapshot().size() == 10)
        self._assert_all_values_between(sample, 1000, 2000)

        twisted_clock.advance(15*3600)
        sample.update(2000)
        self.assertTrue(sample.get_snapshot().size() == 2)
        self._assert_all_values_between(sample, 1000, 3000)

        for i in xrange(1000):
            sample.update(3000 + i)
            twisted_clock.advance(0.1)

        self.assertTrue(sample.get_snapshot().size() == 10)
        self._assert_all_values_between(sample, 3000, 4000)

    def _assert_all_values_between(self, sample, lower, upper):
        for value in sample.get_snapshot().get_values():
            self.assertTrue(value >= lower and value < upper)
