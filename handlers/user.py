# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime

import data

from google.appengine.api import users

from handlers import base

class User(base.Base):
  def get(self):
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
        'user': users.get_current_user(),
        'users': data.get_all_users(),
        'user_id' : user_id
        }
    self.render('user.html', template_values)

  #TODO(kberg): This should really be another URL Path.
  def post(self):
    user = users.get_current_user()
    if user:
	    secret = self.request.get('secret')
	    data.add_user(user.user_id(), user.email(), secret)
