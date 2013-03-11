# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime

import data

from google.appengine.api import users

from handlers import base

import sys

class User(base.Base):
  def get(self):
    template_values = { }
    try:
      current_user = users.get_current_user()
      user = data.get_user_by_id(current_user.user_id())
      template_values['nickname'] = user.nickname
      template_values['secret'] = user.secret

    except Exception as e:
      sys.stderr.write(e)
    
    self.render('user.html', template_values)

# TODO(kberg): this shouldn't extend base.Base, because we don't care about rendering, etc.
class SaveUser(base.Base):
  def post(self):
    secret = self.request.get('secret')
    nickname = self.request.get('nickname')
    user = users.get_current_user()
    uid = user.user_id()
    try:
      data.get_user_by_id(uid)
      data.update_user(uid, secret, nickname)
    except data.UserException:
	    data.add_user(uid, user.email(), secret, nickname)
    self.redirect('/list')
