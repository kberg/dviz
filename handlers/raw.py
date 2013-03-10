# NOTE: NO SECURITY. You can add crap like a series name "<script>alert("!")</script>" and have bad things happen.
#

import datetime

import data

from handlers import base

class RawData(base.Base):
  def get(self, timerange, names):
    # Convert timerange an exact date.
    since = self.get_time_ago(timerange)
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

  def get_time_ago(self, timerange):
    if timerange == 'all':
      return datetime.datetime(1970, 01, 01)
    hours_ago = 0
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
