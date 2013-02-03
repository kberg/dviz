import web
from graphme import Graph
from server_data import Data

web.internalerror = web.debugerror

_t_globals = {
    'user': 'mote',
    }
_render = web.template.render('templates/', cache=False, globals=_t_globals)

class View:
  def GET(self, args=''):
    return 'hello world'

class RobotsTxt:
  def GET(self):
    return ''

if __name__ == '__main__':
  urls = [
      '', 'View',
      '/', 'View',
      '/graph', 'Graph',
      '/data/(.+)', 'Data',
      ]
  application = web.application(urls, globals())
  application.run()

