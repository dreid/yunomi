from __future__ import division, absolute_import

import mock

from unittest2 import TestCase

from yunomi.core.counter import Counter
from threading import Lock


class CounterTests(TestCase):
    def setUp(self):
        Lock_patcher = mock.patch('yunomi.core.counter.Lock', spec=Lock)
        self._lock = Lock_patcher.start().return_value
        self.addCleanup(Lock_patcher.stop)

        self._counter = Counter()

        self._value_on_enter = []

        def enter():
            self._value_on_enter.append(self._counter.get_count())

        self._lock.__enter__.side_effect = enter

        self._value_on_exit = []

        def exit(*args, **kwargs):
            self._value_on_exit.append(self._counter.get_count())

        self._lock.__exit__.side_effect = exit

    def test_starts_at_zero(self):
        self.assertEqual(self._counter.get_count(), 0)

    def test_increments_by_one(self):
        self._counter.inc()
        self.assertEqual(self._counter.get_count(), 1)

    def test_increments_by_arbitrary_delta(self):
        self._counter.inc(12)
        self.assertEqual(self._counter.get_count(), 12)

    def test_decrements_by_one(self):
        self._counter.dec()
        self.assertEqual(self._counter.get_count(), -1)

    def test_decrements_by_arbitrary_delta(self):
        self._counter.dec(12)
        self.assertEqual(self._counter.get_count(), -12)

    def test_is_zero_after_being_cleared(self):
        self._counter.inc()
        self._counter.clear()
        self.assertEqual(self._counter.get_count(), 0)

    def _assert_lock_acquired(self, before, after, f, *args, **kwargs):
        """
        All locks should be used as context managers so this asserts that
        C{__enter__} and C{__exit__} are called.  And that at the time they are
        called, the current value of the object equals C{before} and C{after}.
        """
        f(*args, **kwargs)

        self._lock.__enter__.assert_called_once_with()
        self.assertEqual(self._value_on_enter, [before])

        self._lock.__exit__.assert_called_once_with(None, None, None)
        self.assertEqual(self._value_on_exit, [after])

    def test_inc_locks(self):
        self._assert_lock_acquired(0, 10, self._counter.inc, 10)

    def test_dec_locks(self):
        self._assert_lock_acquired(0, -10, self._counter.dec, 10)

    def test_clear_locks(self):
        self._assert_lock_acquired(0, 0, self._counter.clear)
