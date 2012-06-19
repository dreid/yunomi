from unittest import TestCase

from yunomi.stats.uniform_sample import UniformSample
from yunomi.stats.snapshot import Snapshot


class UniformSampleTests(TestCase):
    def test_aSampleOf1000OutOf1000Elements(self):
        sample = UniformSample(100)
        for i in xrange(1000):
            sample.update(i)
        snapshot = sample.getSnapshot()

        self.assertEqual(sample.size(), 100)
        self.assertEqual(snapshot.size(), 100)

        for i in snapshot.getValues():
            self.assertTrue(i < 1000 and i >=0)
