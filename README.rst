Python client for IERS-OP web service
=====================================

It answers the following questions:

- What is the current difference between TAI and UTC?
- When was the last leap second?
- When is the next leap second?


Usage
-----

As a library::

    >>> from leap_second_client import request_leap_second_info
    >>> request_leap_second_info()
    LeapSecondInfo(TAI_UTC=36,
                   last_leap_second=datetime.date(2015, 6, 30),
                   next_leap_second=None)

Or as a command-line client (greppable json output)::

    $ python -m leap_second_client
    {
        "TAI_UTC": 36,
        "last_leap_second": "2015-06-30",
        "next_leap_second": null
    }

It gives the current value of TAI-UTC in (integer) seconds, the date
of the last leap second and the date of the next leap second. If no
leap second is scheduled, then the value is None. The webservice
relies on the information of the last Bulletin C and the current date.

See http://hpiers.obspm.fr/eop-pc/index.php?index=webservice

Installation
------------

No dependencies except Python itself and the webservice.
To install, just `download leap_second_client.py <https://github.com/zed/leap-second-client/blob/master/leap_second_client.py>`_ or run::

    $ pip install leap_second_client

Support: Python 2.6+, Python 3.

License: MIT
