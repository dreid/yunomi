from unittest import TestCase

from yunomi.core.histogram import Histogram


class HistogramTests(TestCase):

    def setUp(self):
        self.histogram_b = Histogram(Histogram.SampleType.BIASED)
        self.histogram_u = Histogram(Histogram.SampleType.UNIFORM)

    def test_empty_histogram(self):
        for histogram in self.histogram_b, self.histogram_u:
            histogram.clear()
            self.assertEqual(histogram.get_count(), 0)
            self.assertAlmostEqual(histogram.get_max(), 0)
            self.assertAlmostEqual(histogram.get_min(), 0)
            self.assertAlmostEqual(histogram.get_mean(), 0)
            self.assertAlmostEqual(histogram.get_std_dev(), 0)
            self.assertAlmostEqual(histogram.get_sum(), 0)

            snapshot = histogram.get_snapshot()
            self.assertAlmostEqual(snapshot.get_median(), 0)
            self.assertAlmostEqual(snapshot.get_75th_percentile(), 0)
            self.assertAlmostEqual(snapshot.get_99th_percentile(), 0)
            self.assertAlmostEqual(snapshot.size(), 0)

    def test_histogram_with_1000_elements(self):
        for histogram in self.histogram_b, self.histogram_u:
            histogram.clear()
            for i in xrange(1, 1001):
                histogram.update(i)

            self.assertEqual(histogram.get_count(), 1000)
            self.assertAlmostEqual(histogram.get_max(), 1000)
            self.assertAlmostEqual(histogram.get_min(), 1)
            self.assertAlmostEqual(histogram.get_mean(), 500.5)
            self.assertAlmostEqual(histogram.get_std_dev(), 288.8194360957494, places=3)
            self.assertAlmostEqual(histogram.get_sum(), 500500)

            snapshot = histogram.get_snapshot()
            self.assertAlmostEqual(snapshot.get_median(), 500.5)
            self.assertAlmostEqual(snapshot.get_75th_percentile(), 750.75)
            self.assertAlmostEqual(snapshot.get_99th_percentile(), 990.99)
            self.assertAlmostEqual(snapshot.size(), 1000)
