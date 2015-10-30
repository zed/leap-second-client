"""Python client for IERS-OP WEB SERVICE.

This webservice gives the current value of UT1-UTC, the date of the
last leap second and the date of the next leap second. If no leap
second is scheduled, then it outputs "Not scheduled". This webservice
relies on the information of the last Bulletin C and the current date.

http://hpiers.obspm.fr/eop-pc/index.php?index=webservice

No dependencies except Python itself.
"""
import json
import platform
import xml.etree.ElementTree as etree
try:
    from urllib.request import urlopen, Request
except ImportError: # Python 2
    from urllib2 import urlopen, Request

__version__ = '0.0.1'
user_agent = '{}/{} leap_second_client/{}'.format(platform.python_implementation(),
                                                  platform.python_version(),
                                                  __version__)
print(user_agent)
url = "http://hpiers.obspm.fr/eop-pc/webservice/leap_second_server.php"
headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    #XXX quotes inside quotes!
    'SOAPAction': '"http://hpiers.obspm.fr/eop-pc/webservice/leap_second_server.php/LeapSecond"',
    'User-Agent': user_agent,
}
data = '''<?xml version="1.0" encoding="UTF-8"?>
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

def reformat_date(webservice_date_string):
    return str(datetime.strptime(webservice_date_string, '%Y %B %d').date())

response = etree.parse(urlopen(Request(url, data, headers)))
next_leap_second = response.findtext('.//Last_leap_second')
if next_leap_second != "Not scheduled":
    next_leap_second = reformat_date(next_leap_second)
else:
    next_leap_second = None

print(json.dumps(dict(
    TAI_UTC=int(response.findtext('.//TAI_UTC'))
    last_leap_second=reformat_date(response.findtext('.//Last_leap_second')),
    next_leap_second=next_leap_second)))
