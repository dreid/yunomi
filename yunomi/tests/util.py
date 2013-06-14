from __future__ import division, absolute_import


class Clock(object):
    """
    Stripped down version of C{twisted.internet.task.Clock} from Twisted 13.0.0
    """
    rightNow = 0.0

    def seconds(self):
        """
        Pretend to be time.time().

        @rtype: C{float}
        @return: The time which should be considered the current time.
        """
        return self.rightNow

    def advance(self, amount):
        """
        Move time on this clock forward by the given amount.

        @type amount: C{float}
        @param amount: The number of seconds which to advance this clock's
        time.
        """
        self.rightNow += amount


__all__ = [
    Clock
]
