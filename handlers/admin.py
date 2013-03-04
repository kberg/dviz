# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime
import os
import sys
import webapp2

import data

from google.appengine.ext.webapp import template
from google.appengine.api import users

# TODO - add security

class Admin(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'user': users.get_current_user(),
      'entries': data.get_all_series(),
    }

    path = os.path.join(os.path.dirname(__file__), '../templates/admin.html')
    self.response.out.write(template.render(path, template_values))

class Users(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'users': data.get_all_users(),
    }

    path = os.path.join(os.path.dirname(__file__), '../templates/admin_users.html')
    self.response.out.write(template.render(path, template_values))

class User(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'entries': data.get_all_series(),
    }

    path = os.path.join(os.path.dirname(__file__), '../templates/admin/user.html')
    self.response.out.write(template.render(path, template_values))
