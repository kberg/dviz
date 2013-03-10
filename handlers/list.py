# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

# handler for /list

import data

from google.appengine.api import users

from handlers import base

class List(base.Base):
  def get(self):
    template_values = {
      'user': users.get_current_user(),
      'entries': data.get_all_series(),
    }

    self.render('list.html', template_values)
