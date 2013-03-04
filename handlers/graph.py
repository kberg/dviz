# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import data

from google.appengine.api import users

from handlers import base

class Graph(base.Base):
  def get(self, names):
    template_values = {
      'user': users.get_current_user(),
      'series': names
    }
    # only get first. will need to get them all, later.
    latest = data.get_latest_value(names.split(',')[0])
    if latest:
      template_values['latest_val'] = latest.value
      template_values['latest_ts'] = latest.timestamp
    else:
      template_values['latest_val'] = 'NaN'
      template_values['latest_ts'] = 'NaN'

    self.render('graph.html', template_values)
