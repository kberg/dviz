# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import webapp2

from handlers import addrandom
from handlers import admin
from handlers import graph
from handlers import list
from handlers import mainpage
from handlers import newseries
from handlers import push
from handlers import raw
from handlers import series
from handlers import user

app = webapp2.WSGIApplication([
  ('/', mainpage.MainPage),
  ('/user', user.User),
  ('/raw', raw.RawData),
  ('/raw/(.+)/(.+)', raw.RawData),
  ('/list', list.List),
  ('/push', push.Push),
  ('/newseries', newseries.NewSeries),
  ('/random', addrandom.AddRandom),  # for testing only.
  ('/graph/(.+)', graph.Graph),
  ('/s/(.+)', series.Series),

  ('/admin', admin.Admin),
  ('/admin/users', admin.Users),
  ('/admin/user', admin.User)
  ])
