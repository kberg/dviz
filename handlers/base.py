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
  def render(self, name, template_values):
    path = os.path.join(os.path.dirname(__file__), '../templates/%s' % name)
    navbar = { }
    user = { }
    current_user = users.get_current_user()

    # load from the users table to see if the user is registered, and to
    # get user's nickname.
    nickname = ''
    registered = False
    if current_user:
      try:
        nickname = data.get_user_by_id(current_user.user_id()).nickname
        registered = True
      except Exception as e: # Come up with better exception.
        sys.stderr.write(e)
        pass

    if current_user:
      navbar = {
        'email' : current_user.email(),
        'nickname' : nickname
      }
      user = {
        'uid' : current_user.user_id(),
        'email' : current_user.email(),
        'nickname' : nickname,
        'registered' : registered
      }
    else:
      navbar = {
        'email' : '',
        'nickname' : ''
      }
      user = {
        'uid' : '',
        'email' : '',
        'nickname' : '',
        'registered' : False
      }

    template_values['user'] = user

    if current_user and current_user.email():
      navbar['logout_url'] = users.create_logout_url('/')
    else:
      navbar['login_url'] = users.create_login_url('/')

    template_values['navbar'] = navbar
    self.response.out.write(template.render(path, template_values))
