# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

# base handler

import datetime
import os
import sys
import webapp2

import data

from google.appengine.ext.webapp import template
from google.appengine.api import users

class Base(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'entries': data.get_all_series(),
    }

  def render(self, name, template_values):
    path = os.path.join(os.path.dirname(__file__), '../templates/%s' % name)
    navbar = { }
    user = users.get_current_user()
    navbar["email"] = user.email()
    if (user.email):
      navbar["logout_url"] = users.create_logout_url("/")
    else:
      navbar["login_url"] = users.create_login_url("/")

    template_values["navbar"] = navbar
    self.response.out.write(template.render(path, template_values))

