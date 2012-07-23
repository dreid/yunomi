from unittest2 import TestCase

from yunomi.stats.snapshot import Snapshot


class SnapshotTests(TestCase):
    def setUp(self):
        self.snapshot = Snapshot([5, 1, 2, 3, 4])

    def test_small_quantiles_are_the_first_value(self):
        self.assertAlmostEqual(self.snapshot.get_value(0.0), 1)

    def test_big_quantiles_are_the_last_value(self):
        self.assertAlmostEqual(self.snapshot.get_value(1.0), 5)

    def test_has_a_median(self):
        self.assertAlmostEqual(self.snapshot.get_median(), 3)

    def test_percentiles(self):
        percentiles = [(4.5, self.snapshot.get_75th_percentile),
                    (5, self.snapshot.get_98th_percentile),
                    (5, self.snapshot.get_99th_percentile),
                    (5, self.snapshot.get_999th_percentile)]

        for val, func in percentiles:
            self.assertAlmostEqual(func(), val)

    def test_has_values(self):
        self.assertEquals(self.snapshot.get_values(), [1, 2, 3, 4, 5])

    def test_has_a_size(self):
        self.assertEquals(self.snapshot.size(), 5)
