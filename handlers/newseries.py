# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime
import os
import sys
import webapp2

import data

from google.appengine.ext.webapp import template
from google.appengine.api import users

class NewSeries(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    user_id = user.user_id()

    name = self.request.get('name')
    # TODO(konigsberg): Validate/sanitize name
    data.get_or_add_series(name, user_id=user_id)
    # TODO: redirect to /s/name
    self.response.out.write("<a href='/s/%s'>Created, go to it</a>" % name)
