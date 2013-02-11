"Client library to add stuff to dviz."

import urllib
import urllib2
import datetime


class DvizClient:
  def __init__(self, server=None):
    if not server:
      # TODO: later change to just main url.
      self._URL = 'http://localhost:8080/data'
    else:
      self._URL = server
    
  def add(self, series_name, value, timestamp=None, user_name=None,
      user_secret=None):
    data = {
      'series': series_name,
      'value': value,
      'timestamp': timestamp,
      'user_name': user_name,
      'user_secret': user_secret,
      }
    pdata = urllib.urlencode(data)
    req = urllib2.Request(self._URL, pdata)
    resp = urllib2.urlopen(req)
    return resp.read()
  

if __name__ == '__main__':
  dc = DvizClient()
  print dc.add('foo', 42.0)
  #print dc.add('foo', 45, datetime.datetime(2012, 02, 1, 9, 45))

