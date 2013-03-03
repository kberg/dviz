# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime
import os
import sys
import webapp2

import data

from google.appengine.ext.webapp import template
from google.appengine.api import users

class Push(webapp2.RequestHandler):
  def get(self):
    self.post()

  def post(self):
    # TODO: need to authenticate w/ User secret.
    name = self.request.get('name')
    secret = self.request.get('secret')
    series = self.request.get('series')
    value = float(self.request.get('value'))
    timestamp = self.request.get('timestamp')
    timems = self.request.get('timems')
    if not timestamp or timestamp == 'None' or timestamp == '':
      if timems and timems != '':
        timeSeconds = float(timems) / 1000
        timestamp = datetime.datetime.utcfromtimestamp(timeSeconds)
      else:
        timestamp = datetime.datetime.now()
    else:
      # kberg asks: IS THIS RIGHT?
      timestamp = datetime.strptime('%Y/%m/%d %H:%M:%S')
    data.add(series, value, timestamp)
    self.response.out.write('Added: %s, %s, %s\n' % (
      series, value, timestamp))
