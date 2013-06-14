from __future__ import division, absolute_import
from threading import RLock

class Counter(object):
    """
    A counter method that increments and decrements.
    """
    def __init__(self):
        """
        Create a new instance of a L{Counter}.
        """
        self._count = 0
        self._lock = RLock()

    def inc(self, n=1):
        """
        Increment the counter by I{n}.

        @type n: C{int}
        @param n: the amount to be incremented
        """
        with self._lock:
            self._count += n

    def dec(self, n=1):
        """
        Decrement the counter by I{n}.

        @type n: C{int}
        @param n: the amount to be decrement
        """
        with self._lock:
            self._count -= n

    def get_count(self):
        """
        Returns the count

        @rtype: C{int}
        @return: the count
        """
        return self._count

    def clear(self):
        """
        Resets the count back to 0.
        """
        with self._lock:
            self._count = 0
