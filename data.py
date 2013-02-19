import datetime
import sys

from google.appengine.ext import db
from google.appengine.ext import ndb


class User(db.Model):
  uid = db.StringProperty()      # username
  secret = db.StringProperty()   # secret key for POSTing.
                                 # TODO: salt.


class Series(db.Model):
  name = db.StringProperty()
  timestamp = db.DateTimeProperty(auto_now=True)
  owner = db.ReferenceProperty(User)
  # TODO: add visibility rules.
  # Maybe just a bool externally-visible flag, or maybe something more
  # complicated like a list of users that have read/write privs.


class SeriesData(db.Model):
  series = db.ReferenceProperty(Series)
  timestamp = db.DateTimeProperty()
  value = db.FloatProperty()


def get_user(user_id='', secret=''):
  if secret:
    return get_user_by_secret(secret)
  if user_id:
    return get_user_by_id(user_id)
  return


def get_user_by_id(user_id):
  try:
    return User.gql('WHERE uid =:1', user_id)[0]
  except IndexError:
    return None


def get_user_by_secret(secret):
  try:
    return User.gql('WHERE secret =:1', secret)[0]
  except IndexError:
    return None


def add_user(user_id, secret):
  # TODO: should raise exceptions here probably.
  # Don't create a dupe user
  if get_user_by_id(user_id):
    return
  # likewise, secret should be unique.
  if get_user_by_secret(secret):
    return
  u = User(uid=user_id, secret=secret)
  u.put()


def get_all_users():
  return User.all().run()


def get_series_by_name(name, user=None):
  # TODO: enforce user ACL.
  try:
    return Series.gql('WHERE name =:1', name)[0]
  except IndexError:
    return None


def get_or_add_series(user, name):
  """Gets a series, or adds it if it doesn't exist."""
  series = get_series_by_name(user, name)
  if not series:
    series = Series(name=name, owner=user)
    series.put()
  return series


def get_all_series():
  return Series.all().run()


def get_all_series_for_user(user_id):
  u = get_user_by_id(user_id)
  if not u:
    return []
  return Series.all().filter('owner =', user).run() 


def get_series_data(name, since):
  """Get all data from a series."""
  series = get_series_by_name(name)
  if not series:
    return []
  return SeriesData.all().filter(
    'series =', series).filter(
    'timestamp > ', since).order('-timestamp').run()

def get_latest_value(name):
  series = get_series_by_name(name)
  if not series:
    return None
  try:
    return list(SeriesData.all().filter('series =', series).order('-timestamp').fetch(1))[0]
  except Exception, e:
    return None


def get_multiple_series_data(names, since):
  """Get all data from multiple serieses."""
  serieses = [get_series_by_name(n) for n in names]
  serieses = [s for s in serieses if s]
  if not serieses:
    return []
  return SeriesData.all().filter(
      'series IN ', serieses).filter(
      'timestamp > ', since).order('-timestamp')


def add(name, value, user_id='', secret='', timestamp=None):
  user = get_user(user_id, secret_)
  series = get_or_add_series(user, name)
  if not series:
    # Bad user?  fail silently.
    return
  d = SeriesData(series=series, value=value)
  if not timestamp:
    timestamp = datetime.datetime.now()
  d.timestamp = timestamp
  d.put()


