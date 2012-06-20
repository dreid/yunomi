from unittest import TestCase

from yunomi.stats.exp_decay_sample import ExponentiallyDecayingSample
from yunomi.stats.snapshot import Snapshot


class ExponentialDecaySapmleTests(TestCase):

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
