import web

_render = web.template.render('templates/', cache=False)

class Graph:
  def GET(self, series):
    return _render.graph(series) # set series
