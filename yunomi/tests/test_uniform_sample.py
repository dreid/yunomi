from __future__ import division, absolute_import

from unittest2 import TestCase

from yunomi.compat import xrange
from yunomi.stats.uniform_sample import UniformSample


class UniformSampleTests(TestCase):

    def test_a_sample_of_100_out_of_1000_elements(self):
        sample = UniformSample(100)
        for i in xrange(1000):
            sample.update(i)
        snapshot = sample.get_snapshot()

        self.assertEqual(sample.size(), 100)
        self.assertEqual(snapshot.size(), 100)

        for i in snapshot.get_values():
            self.assertTrue(i < 1000 and i >= 0)
