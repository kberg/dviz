# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime
import data

from google.appengine.api import users

from handlers import base

class Push(base.Base):
  def get(self):
    self.post()

  def post(self):
    secret = self.request.get('secret')
    try:
      user = users.get_current_user()
      user_id = user.user_id()
    except:
      user_id = None

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
    data.add(name=series, value=value, timestamp=timestamp, user_id=user_id,
        secret=secret)
    self.response.out.write('Added: %s, %s, %s\n' % (
      series, value, timestamp))
