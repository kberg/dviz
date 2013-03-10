#!/usr/bin/python
"Client library to add stuff to dviz."

import urllib
import urllib2
import datetime


class DvizClient:
  def __init__(self, server=None):
    if not server:
      # TODO: later change to just main url.
      self._URL = 'http://localhost:8080/push'
    else:
      self._URL = server
    
  def add(self, series_name, value, timestamp=None, user_secret=None):
    data = {
      'series': series_name,
      'value': value,
      'timestamp': timestamp,
      'user_secret': user_secret,
      }
    pdata = urllib.urlencode(data)
    req = urllib2.Request(self._URL, pdata)
    resp = urllib2.urlopen(req)
    return resp.read()
  

if __name__ == '__main__':
  dc = DvizClient()
  value = datetime.datetime.now().second
  print dc.add(series_name='from_client', value=value, user_secret='foo')

