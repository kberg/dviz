# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import webapp2

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.redirect("/list")
