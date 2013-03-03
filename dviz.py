# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime
import os
import random
import sys
import webapp2

import data

from google.appengine.ext.webapp import template
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.redirect("/list")

class User(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'templates/user.html')
    user = users.get_current_user()
    if user:
      link = users.create_logout_url(self.request.uri)
      link_text = 'Logout'
    else:
      link = users.create_login_url(self.request.uri)
      link_text = 'Login'

    if user:
      user_id = user.user_id()
    else:
      user_id = ''
    template_values = {
        'link': link,
        'link_text' : link_text,
        'users': data.get_all_users(),
        'user_id' : user_id
        }
    self.response.out.write(template.render(path, template_values))

  def post(self):
    #sys.stderr.write(' '.join(self.request.get_all()))
    user_id = self.request.get('user_id')
    secret = self.request.get('secret')
    data.add_user(user_id, secret)


class Graph(webapp2.RequestHandler):
  def get(self, names):
    template_values = {
      'series': names
    }
    # only get first. will need to get them all, later.
    latest = data.get_latest_value(names.split(',')[0])
    if latest:
      template_values['latest_val'] = latest.value
      template_values['latest_ts'] = latest.timestamp
    else:
      template_values['latest_val'] = 'NaN'
      template_values['latest_ts'] = 'NaN'


    path = os.path.join(os.path.dirname(__file__), 'templates/graph.html')
    self.response.out.write(template.render(path, template_values))


def get_time_ago(timerange):
  if timerange == 'hour':
    hours_ago = 1
  if timerange == 'day':
    hours_ago = 24
  if timerange == 'week':
    hours_ago = 24*7
  if timerange == 'month':
    hours_ago = 24*30
  if timerange == 'year':
    hours_ago = 24*365
  return datetime.datetime.now() - datetime.timedelta(hours=hours_ago)


class Data(webapp2.RequestHandler):
  def get(self, timerange, names):
    # Convert timerange an exact date.
    since = get_time_ago(timerange)
    names = names.split(',')
    text = ''
    if len(names) == 0:
      text = ''
    elif len(names) == 1:
      self.response.out.write('Date,%s\n' % names[0])
      points = list(data.get_series_data(names[0], since))
      for point in points:
        self.response.out.write('%s,%f\n' % (
            point.timestamp.strftime('%Y/%m/%d %H:%M:%S'),
            point.value))
    else:
      self.response.out.write('Date,%s\n' % ','.join(names))
      points = list(data.get_multiple_series_data(names, since))

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
   now = datetime.datetime.now()
   for i in range(20):

     # add a few in last hour, day, week, month, year.
     hour_secs = 60*60
     day_secs = 24*hour_secs
     week_secs = 7*day_secs
     month_secs = 30*day_secs
     year_secs = 365*day_secs

     for ago in (hour_secs, day_secs, week_secs, month_secs, year_secs):
       data.add('first',
           float(random.randint(0, 100)),
           now - datetime.timedelta(seconds=ago))
       data.add('second',
           float(random.randint(0, 100)),
           now - datetime.timedelta(seconds=ago))



class NewSeries(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    user_id = user.user_id()

    name = self.request.get('name')
    # TODO(konigsberg): Validate/sanitize name
    data.get_or_add_series(name, user_id=user_id)
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
  ('/user', User),
  ('/data', Data),
  ('/data/(.+)/(.+)', Data),
  ('/list', List),
  ('/push', Push),
  ('/newseries', NewSeries),
  ('/random', AddRandom),  # for testing only.
  ('/graph/(.+)', Graph),
  ('/s/(.+)', Series)
  ])
