# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime
import os
import sys
import webapp2

import data

from google.appengine.ext.webapp import template
from google.appengine.api import users

class User(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), '../templates/user.html')
    user = users.get_current_user()
    if user:
      link = users.create_logout_url(self.request.uri)
      link_text = 'Logout'
    else:
      link = users.create_login_url(self.request.uri)
      link_text = 'Login'

    if user:
      user_id = user.user_id()
    else:
      user_id = ''
    template_values = {
        'link': link,
        'link_text' : link_text,
        'users': data.get_all_users(),
        'user_id' : user_id
        }
    self.response.out.write(template.render(path, template_values))

  def post(self):
    #sys.stderr.write(' '.join(self.request.get_all()))
    user_id = self.request.get('user_id')
    secret = self.request.get('secret')
    data.add_user(user_id, secret)
