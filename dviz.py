# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime
import random
import os
import sys

import webapp2

import data

from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.redirect("/list")

class Graph(webapp2.RequestHandler):
  def get(self, names):
    template_values = {
      'series': names
    }

    path = os.path.join(os.path.dirname(__file__), 'templates/graph.html')
    self.response.out.write(template.render(path, template_values))

class Data(webapp2.RequestHandler):
  def get(self, names):
    sys.stderr.write('get.\n')
    names = names.split(',')
    text = ''
    if len(names) == 0:
      text = ''
    elif len(names) == 1:
      self.response.out.write('Date,%s\n' % names[0])
      points = list(data.get_series_data(names[0]))
      for point in points:
        self.response.out.write('%s,%f\n' % (
            point.timestamp.strftime('%Y/%m/%d %H:%M:%S'),
            point.value))
    else:
      self.response.out.write('Date,%s\n' % ','.join(names))
      points = list(data.get_multiple_series_data(names))

      cur_points = {}
      last_timestamp = None
      for i in range(len(points)):
        point = points[i]
        if last_timestamp and last_timestamp != point.timestamp:
          values = ['%s' % cur_points.get(n, 'None') for n in names]
          self.response.out.write('%s,%s\n' % (
            last_timestamp.strftime('%Y/%m/%d %H:%M:%S'),
            ','.join(values)))
          cur_points = {point.series.name : point.value}
          last_timestamp = point.timestamp
        else:
          if not last_timestamp:
            last_timestamp = point.timestamp
          cur_points[point.series.name] = point.value
      if last_timestamp:
        values = ['%s' % cur_points.get(n, 'None') for n in names]
        self.response.out.write('%s,%s\n' % (
          last_timestamp.strftime('%Y/%m/%d %H:%M:%S'),
          ','.join(values)))

class Push(webapp2.RequestHandler):
  def get(self):
    self.post()

  def post(self):
    # TODO: need to authenticate w/ User secret.
    name = self.request.get('name')
    secret = self.request.get('secret')
    series = self.request.get('series')
    value = float(self.request.get('value'))
    timestamp = self.request.get('timestamp')
    timems = self.request.get('timems')
    if not timestamp or timestamp == 'None' or timestamp == '':
      if timems and timems != '':
        timeSeconds = float(timems) / 1000
        timestamp = datetime.datetime.utcfromtimestamp(timeSeconds)
      else:
        timestamp = datetime.datetime.now()
    else:
      # kberg asks: IS THIS RIGHT?
      timestamp = datetime.strptime('%Y/%m/%d %H:%M:%S')
    data.add(series, value, timestamp)
    self.response.out.write('Added: %s, %s, %s\n' % (
      series, value, timestamp))

class List(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'entries': data.get_all_series(),
    }

    path = os.path.join(os.path.dirname(__file__), 'templates/list.html')
    self.response.out.write(template.render(path, template_values))


 
class AddRandom(webapp2.RequestHandler):
  def get(self):
   self.response.out.write('adding random data.')
   for i in range(100):
     month = random.randint(1, 12)
     day = random.randint(1, 27)
     timestamp = datetime.datetime(year=2012, month=month, day=day)
     data.add('first', float(random.randint(0, 100)), timestamp)
     data.add('second', float(random.randint(0, 100)), timestamp)

class NewSeries(webapp2.RequestHandler):
  def get(self):
    name = self.request.get('name')
    # TODO(konigsberg): Validate/sanitize name
    data.get_or_add_series(name)
    # TODO: redirect to /s/name
    self.response.out.write("<a href='/s/%s'>Created, go to it</a>" % name)

class Series(webapp2.RequestHandler):
  def get(self, name):
    template_values = {
      'name' : name
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/series.html')
    self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/data', Data),
  ('/data/(.+)', Data),
  ('/list', List),
  ('/push', Push),
  ('/newseries', NewSeries),
  ('/random', AddRandom),  # for testing only.
  ('/graph/(.+)', Graph),
  ('/s/(.+)', Series)
  ])
