#!/usr/bin/env python
"""Python client for IERS-OP WEB SERVICE.

As a library:

  >>> from leap_second_client import request_leap_second_info
  >>> request_leap_second_info()
  LeapSecondInfo(TAI_UTC=36,
                 last_leap_second=datetime.date(2015, 6, 30),
                 next_leap_second=None)

Or as a command-line client (greppable json output):

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

No dependencies except Python itself and the webservice.
To install, just download leap_second_client.py.
Support: Python 2.6+, Python 3.

"""
import json
import platform
import xml.etree.ElementTree as etree
from collections import namedtuple
from datetime import datetime

try:
    from urllib.request import urlopen, Request
except ImportError:  # Python 2
    from urllib2 import urlopen, Request


__all__ = ['request_leap_second_info']
__version__ = '1.0'

LeapSecondInfo = namedtuple('LeapSecondInfo',
                            'TAI_UTC last_leap_second next_leap_second')

_url = "http://hpiers.obspm.fr/eop-pc/webservice/leap_second_server.php"
_user_agent = 'leap_second_client/%s %s/%s' % (
    __version__,
    platform.python_implementation(),
    platform.python_version())
_headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': '"http://hpiers.obspm.fr/eop-pc/webservice/'
                  'leap_second_server.php/LeapSecond"',
    'User-Agent': _user_agent,
}
_data = '''<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
   xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
   xmlns:ns0="http://hpiers.obspm.fr/eop-pc/webservice/"
   xmlns:ns1="http://schemas.xmlsoap.org/soap/encoding/"
   xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:ns2="http://schemas.xmlsoap.org/soap/envelope/"
   SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <SOAP-ENV:Header/>
  <ns2:Body>
    <ns0:LeapSecond/>
  </ns2:Body>
</SOAP-ENV:Envelope>
'''.encode()


def _parse_date(webservice_date_string):
    return datetime.strptime(webservice_date_string, '%d %B %Y').date()


def _parse_next_leap_date(webservice_date_string):
    return datetime.strptime(webservice_date_string, '%Y %B %d, 23h 59m 60s').date()


def request_leap_second_info():
    """Make request to the IERS-OP leap second webservice."""
    response = etree.parse(urlopen(Request(_url, _data, _headers)))
    next_leap_second = response.findtext('.//Next_leap_second')
    if next_leap_second != "Not scheduled":
        next_leap_second = _parse_next_leap_date(next_leap_second)
    else:
        next_leap_second = None
    return LeapSecondInfo(
        TAI_UTC=int(response.findtext('.//TAI_UTC')),
        last_leap_second=_parse_date(response.findtext('.//Last_leap_second')),
        next_leap_second=next_leap_second)


def main():
    print(json.dumps(request_leap_second_info()._asdict(),
                     indent=4, default=str, sort_keys=True))


if __name__ == "__main__":
    main()
