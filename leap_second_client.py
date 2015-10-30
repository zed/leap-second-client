"""Python client for IERS-OP WEB SERVICE.

This webservice gives the current value of UT1-UTC, the date of the
last leap second and the date of the next leap second. If no leap
second is scheduled, then it ouputs "Not scheduled". This webservice
relies on the information of the last Bulletin C and the current date.

http://hpiers.obspm.fr/eop-pc/index.php?index=webservice
"""
import logging
logging.basicConfig(level=logging.INFO)


from suds.client import Client # $ pip install suds-jurko
logging.getLogger('suds').setLevel(logging.DEBUG)

url = "http://hpiers.obspm.fr/eop-pc/webservice/leap_second_server.php?wsdl"
client = Client(url)
print(client)
result = client.service.LeapSecond()
print('*'*60)
print(result)
print(result.TAI_UTC)
print(result.Last_leap_second)
print(result.Next_leap_second)
