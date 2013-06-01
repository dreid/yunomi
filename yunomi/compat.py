from __future__ import division, absolute_import

import sys


if sys.version_info < (3, 0):
    _PY3 = False
    xrange = xrange

    def dict_item_iter(d):
        """
        Return an iterator over the dict items.
        """
        return d.iteritems()
else:
    _PY3 = True
    xrange = range

    def dict_item_iter(d):
        """
        Return an iterator over the dict items.
        """
        return d.items()


__init__ = [
    _PY3, xrange, dict_item_iter
]
