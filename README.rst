YUNOMI: Y U NO MEASURE IT
=========================

.. image:: https://badge.fury.io/py/yunomi.png
    :target: http://badge.fury.io/py/yunomi

.. image:: https://secure.travis-ci.org/dreid/yunomi.png?branch=master
        :target: http://travis-ci.org/dreid/yunomi

As in:

   It has performance implications, Y U NO MEASURE IT!?

Yunomi provides insights to the internal behavior of an application, providing useful statistics and metrics on selected portions of your code.
It’s a Python port of the core portion of a `Java Metrics library by Coda Hale <http://metrics.codahale.com/>`_.

Stop guessing, start measuring:
   
.. code-block:: bash

   $ pip install yunomi

Core Features
-------------

Counter
+++++++

Simple interface to increment and decrement a value.
For example, this can be used to measure the total number of jobs sent to the queue, as well as the pending (not yet complete) number of jobs in the queue.
Simply increment the counter when an operation starts and decrement it when it completes.

Meter
+++++

Measures the rate of events over time.
Useful to track how often a certain portion of your application gets requests so you can set resources accordingly.
Tracks the mean rate (the overall rate since the meter was reset) and the rate statistically significant regarding only events that have happened in the last 1, 5, and 15 minutes (Exponentially weighted moving average).

Histogram
+++++++++

Measures the statistical distribution of values in a data stream.
Keeps track of minimum, maximum, mean, standard deviation, etc.
It also measures median, 75th, 90th, 95th, 98th, 99th, and 99.9th percentiles.
An example use case would be for looking at the number of daily logins for 99 percent of your days, ignoring outliers.

Timer
+++++

A useful combination of the Meter and the Histogram letting you measure the rate that a portion of code is called and a distribution of the duration of an operation.
You can see, for example, how often your code hits the database and how long those operations tend to take.


Examples
--------

Decorators
++++++++++

The simplest and easiest way to use the yunomi library.

Counter
^^^^^^^

You can use the `count_calls` decorator to count the number of times a function is called.

.. code-block:: pycon

    >>> from yunomi import counter, count_calls
    >>> @count_calls
    ... def test():
    ...     pass
    ... 
    >>> for i in xrange(10):
    ...     test()
    ... 
    >>> print counter("test_calls").get_count()
    10

Timer
^^^^^

You can use the `time_calls` decorator to time the execution of a function and get distributtion data from it.

.. code-block:: pycon

    >>> import time
    >>> from yunomi import timer, time_calls
    >>> @time_calls
    ... def test():
    ...     time.sleep(0.1)
    ... 
    >>> for i in xrange(10):
    ...     test()
    ... 
    >>> print timer("test_calls").get_mean()
    0.100820207596


Requirements
------------

Yunomi has no external dependencies and runs on PyPy and Python 2.6, 2.7, and 3.3.
