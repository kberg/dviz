import datetime
import random
import os


import webapp2

import data
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
    names = names.split(',')
    text = ''
    if len(names) == 0:
      text = ''
    elif len(names) == 1:
      self.response.out.write('Date,%s\n' % names[0])
      points = list(data.get_series_data(names[0]))
      for i in range(len(points)):
        point = points[i]
        self.response.out.write('%s,%f\n' % (
            point.timestamp.strftime('%Y/%m/%d %H:%M:%S'),
            point.value))
    else:
      self.response.out.write('Date,%s\n' % names)
      # TODO: support multi-series data.
      # Should look like (date,data1,data2)
  
  def post(self):
    # TODO: write me.


class Series(webapp2.RequestHandler):
  def get(self):
    html = ['<html><title>all series</title><body>\n<ul>']
    for series in data.get_all_series():
      html.append('<li>%s</li>' % series.name)
    html.append('</ul></body></html>')
    self.response.out.write('\n'.join(html))


class AddRandom(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('adding random data.')
    for i in range(100):
      month = random.randint(1, 12)
      day = random.randint(1, 27)
      timestamp = datetime.datetime(year=2012, month=month, day=day)
      data.add('first', float(random.randint(0, 100)), timestamp)
      data.add('second', float(random.randint(0, 100)), timestamp)



app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/data/(.+)', Data),
  ('/series', Series),
  ('/random', AddRandom),  # for testing only.
  ('/graph/(.+)', Graph),
  ])
