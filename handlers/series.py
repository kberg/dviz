# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

from google.appengine.api import users

from handlers import base

class Series(base.Base):
  def get(self, name):
    template_values = {
      'user': users.get_current_user(),
      'name' : name
    }
    self.render('series.html', template_values)
