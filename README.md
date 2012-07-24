# YUNOMI - Y U NO MEASURE IT

[![Build Status](https://secure.travis-ci.org/dreid/yunomi.png?branch=master)](http://travis-ci.org/dreid/yunomi)

As in:

![Y U NO MEASURE IT](http://cdn.memegenerator.net/instances/400x/22184566.jpg)


A Python port of the core portion of a [Java Metrics library by Coda Hale](http://metrics.codahale.com/)

Yunomi provides insights to the internal behavior of an application, providing useful statistics and metrics on selected portions of your code.

## Core Features

### Counter
Simple interface to increment and decrement a value. For example, this can be used to measure the total number of jobs sent to the queue, as well as the pending (not yet complete) number of jobs in the queue. Simply increment the counter when an operation starts and decrement it when it completes.

### Meter
Measures the rate of events over time. Useful to track how often a certain portion of your application gets requests so you can set resources accordingly. Tracks the mean rate (the overall rate since the meter was reset) and the rate statistically significant regarding only events that have happened in the last 1, 5, and 15 minutes (Exponentally weighted moving average).

### Histogram
Measures the statistical distribution of values in a data stream. Keeps track of minimum, maximum, mean, standard deviatoin, etc. It also measures median, 75th, 90th, 95th, 98th, 99th, and 99.9th percentiles. An example use case would be for looking at the number of daily logins for 99 percent of your days, ignoring outliers.

### Timer
A useful combination of the Meter and the Histogram letting you measure the rate that a portion of code is called and a distribution of the duration of an operation. You can see, for example, how often your code hits the database and how long those operations tend to take.