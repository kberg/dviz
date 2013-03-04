# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime
import os
import sys
import webapp2

import data

from google.appengine.ext.webapp import template
from google.appengine.api import users

class Graph(webapp2.RequestHandler):
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


    path = os.path.join(os.path.dirname(__file__), '../templates/graph.html')
    self.response.out.write(template.render(path, template_values))
