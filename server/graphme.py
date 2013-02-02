import web

_render = web.template.render('templates/', cache=False)

class Graph:
  def GET(self):
    user_data = web.input()
    return _render.graph(user_data.name, 't1-high:t1-low') # set series
