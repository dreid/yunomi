from unittest import TestCase

from yunomi.stats.snapshot import Snapshot


class SnapShotTests(TestCase):
    snapshot = Snapshot([5, 1, 2, 3, 4])

    def test_smallQuantilesAreTheFirstValue(self):
        self.assertAlmostEqual(self.snapshot.getValue(0.0), 1)

    def test_bigQuantilesAreTheLastValue(self):
        self.assertAlmostEqual(self.snapshot.getValue(1.0), 5)

    def test_hasAMedian(self):
        self.assertAlmostEqual(self.snapshot.getMedian(), 3)

    def test_percentiles(self):
        percentiles = [(4.5, self.snapshot.get75thPercentile),
                    (5, self.snapshot.get98thPercentile),
                    (5, self.snapshot.get99thPercentile),
                    (5, self.snapshot.get999thPercentile)]

        for val, func in percentiles:
            self.assertAlmostEqual(func(), val)

    def test_hasValues(self):
        self.assertEquals(self.snapshot.getValues(), [1, 2, 3, 4, 5])

    def test_hasASize(self):
        self.assertEquals(self.snapshot.size(), 5)
