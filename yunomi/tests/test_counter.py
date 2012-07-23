from unittest2 import TestCase

from yunomi.core.counter import Counter


class CounterTests(TestCase):
    _counter = Counter()

    def test_starts_at_zero(self):
        self.assertEqual(self._counter.get_count(), 0)

    def test_increments_by_one(self):
        self._counter.inc()
        self.assertEqual(self._counter.get_count(), 1)
        self._counter.clear()

    def test_increments_by_arbitrary_delta(self):
        self._counter.inc(12)
        self.assertEqual(self._counter.get_count(), 12)
        self._counter.clear()

    def test_decrements_by_one(self):
        self._counter.dec()
        self.assertEqual(self._counter.get_count(), -1)
        self._counter.clear()

    def test_decrements_by_arbitrary_delta(self):
        self._counter.dec(12)
        self.assertEqual(self._counter.get_count(), -12)
        self._counter.clear()

    def test_is_zero_after_being_cleared(self):
        self._counter.clear()
        self.assertEqual(self._counter.get_count(), 0)
