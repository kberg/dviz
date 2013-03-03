# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime
import os
import sys
import webapp2

import data

from google.appengine.ext.webapp import template
from google.appengine.api import users

class Series(webapp2.RequestHandler):
  def get(self, name):
    template_values = {
      'name' : name
    }
    path = os.path.join(os.path.dirname(__file__), '../templates/series.html')
    self.response.out.write(template.render(path, template_values))
