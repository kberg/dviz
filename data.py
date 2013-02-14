import datetime
from google.appengine.ext import db
from google.appengine.ext import ndb

class Series(db.Model):
  name = db.StringProperty()
  timestamp = db.DateTimeProperty(auto_now=True)


class SeriesData(db.Model):
  series = db.ReferenceProperty(Series)
  timestamp = db.DateTimeProperty()
  value = db.FloatProperty()


class User(db.Model):
  uid = db.StringProperty()      # username
  secret = db.StringProperty()   # secret key for POSTing.
  # TODO: need to do stuff with this class.


def get_series_by_name(name):
  try:
    return Series.gql('WHERE name =:1', name)[0]
  except IndexError:
    return None


def get_series_data(name):
  """Get all data from a series."""
  series = get_series_by_name(name)
  if not series:
    return []
  return SeriesData.all().filter('series =', series).order('timestamp').run()

def get_multiple_series_data(names):
  """Get all data from multiple serieses."""
  serieses = [get_series_by_name(n) for n in names]
  serieses = [s for s in serieses if s]
  if not serieses:
    return []
  return SeriesData.all().filter('series IN ', serieses).order('timestamp')


def get_or_add_series(name):
  """Gets a series, or adds it if it doesn't exist."""
  series = get_series_by_name(name)
  if not series:
    series = Series(name=name)
    series.put()
  return series


def get_all_series():
  return Series.all().run()


def add(name, value, timestamp=None):
  series = get_or_add_series(name)
  d = SeriesData(series=series, value=value)
  if not timestamp:
    timestamp = datetime.datetime.now()
  d.timestamp = timestamp
  d.put()


