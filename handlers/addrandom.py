# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#
#  Handler for /random

import datetime
import os
import random
import sys
import webapp2

import data

class AddRandom(webapp2.RequestHandler):
  def get(self):
   self.response.out.write('adding random data.')
   now = datetime.datetime.now()
   for i in range(20):

     # add a few in last hour, day, week, month, year.
     hour_secs = 60*60
     day_secs = 24*hour_secs
     week_secs = 7*day_secs
     month_secs = 30*day_secs
     year_secs = 365*day_secs

     for ago in (hour_secs, day_secs, week_secs, month_secs, year_secs):
       data.add('first',
           float(random.randint(0, 100)),
           now - datetime.timedelta(seconds=ago))
       data.add('second',
           float(random.randint(0, 100)),
           now - datetime.timedelta(seconds=ago))
