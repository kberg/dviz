from google.appengine.ext import db

class Series(db.Model):
  name = db.StringProperty()
  timestamp = db.DateTimeProperty(auto_now=True)

class SeriesData(db.Model):
  series = db.ReferenceProperty(Series)
  timestamp = db.DateTimeProperty(auto_now=True)
  value = db.FloatProperty()


def get_series_data(name):
  """Get all data from a series."""
  #series = db.GqlQuery('SELECT __key__ from 
