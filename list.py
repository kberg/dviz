import web
import datastore

_render = web.template.render('templates/', cache=False)

class List:
  def GET(self):
    l = datastore.Datastore().list()
    return _render.list(l)
