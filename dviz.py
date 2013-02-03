import os

import webapp2
#import template

#TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('Hello world.')


class Graph(webapp2.RequestHandler):
  def get(self, names):
    text = """
    <!DOCTYPE html>
    <html>
      <head>
        <script type='text/javascript'
        src='/static/dygraph-combined.js'></script>
      </head>
      <body>
        <h2>Graph for %s</h2>
        <div id='graph'></div>
        <script type='text/javascript'>
          var g = new Dygraph('graph',
              '/data/%s',
              { });
        </script>
      </body>
    </html>
    """ % (names, names)
    self.response.out.write(text)


class Data(webapp2.RequestHandler):
  def get(self, names):
    data = """Date,taipei_temp,94303_temp
2013/02/02 11:05:00,71.6,51.8
2013/02/02 14:30:00,71.6,55.4
2013/02/02 07:45:00,71.6,50.0
2013/02/02 12:55:00,71.6,53.6
2013/02/02 11:00:00,71.6,51.8
2013/02/02 07:20:00,69.8,50.0
2013/02/02 09:55:00,71.6,51.8
2013/02/02 07:15:00,69.8,50.0
2013/02/02 13:10:00,71.6,53.6
2013/02/02 11:25:00,71.6,51.8
2013/02/02 07:10:00,69.8,50.0
2013/02/02 14:05:00,71.6,53.6
2013/02/02 14:25:00,71.6,55.4
2013/02/02 13:00:00,71.6,53.6
2013/02/02 12:25:00,71.6,53.6
2013/02/02 08:30:00,71.6,50.0
2013/02/02 12:40:00,71.6,53.6
2013/02/02 11:15:00,71.6,51.8
2013/02/02 09:31:00,69.8,51.8
2013/02/02 15:15:00,69.8,55.4
2013/02/02 09:40:00,71.6,51.8
2013/02/02 15:20:00,69.8,55.4
2013/02/02 07:00:00,69.8,50.0
2013/02/02 14:15:00,71.6,55.4
2013/02/02 10:20:00,71.6,51.8
2013/02/02 14:55:00,69.8,55.4
2013/02/02 10:25:00,71.6,51.8
2013/02/02 07:25:00,69.8,50.0
2013/02/02 15:00:00,69.8,55.4
2013/02/02 10:05:00,71.6,51.8
    """
    #self.response.out.write('Data for %s.' % names)
    self.response.out.write(data)


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/data/(.+)', Data),
  ('/graph/(.+)', Graph),
  ])

"""
def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
"""
