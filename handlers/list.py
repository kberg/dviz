# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

# handler for /list

import datetime
import os
import sys
import webapp2

import data

from google.appengine.ext.webapp import template
from google.appengine.api import users

from handlers import addrandom

class List(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'user': users.get_current_user(),
      'entries': data.get_all_series(),
    }

    path = os.path.join(os.path.dirname(__file__), '../templates/list.html')
    self.response.out.write(template.render(path, template_values))
