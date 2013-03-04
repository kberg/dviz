# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import data

from google.appengine.api import users

from handlers import base

# TODO - add security

class Admin(base.Base):
  def get(self):
    template_values = {
      'user': users.get_current_user(),
      'entries': data.get_all_series(),
    }

    self.render('admin.html', template_values)

class Users(base.Base):
  def get(self):
    template_values = {
      'users': data.get_all_users(),
    }

    self.render('admin_users.html', template_values)

class User(base.Base):
  def get(self):
    template_values = {
      'entries': data.get_all_series(),
    }

    self.render('admin_user.html', template_values)
