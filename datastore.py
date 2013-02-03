class Datastore:
  def _topath(self, name):
    return 'teststore/%s.tsv' % name

  def add(self, name, timestamp, value):
    f = open(self._topath(name), 'a')
    f.write('%s\t%s\n' % (timestamp, value))
    f.close()

  def get(self, name):
    """return all data points for name, sorted by timestamp.
    Returns:
       list of (int timestmap, int value) tuples.
    """
    data = [line.split() for line in open(self._topath(name))]
    data = [(int(x), y) for (x, y) in data]
    return sorted(data)

  def getmany(self, names):
    """return merged data from datastore for multiple names.
    Returns:
      list of (int timestamp, int value, int value...) tuples
      if a data point is missing then use None.
    """
    raw_data = [self.get(name) for name in names]
    num_names = len(names)
    processed = dict()
    for index, singlename in enumerate(raw_data):
      for timestamp, value in singlename:
        if not timestamp in processed:
          processed[timestamp] = [''] * num_names
        processed[timestamp][index] = value
    for timestamp, data in processed.iteritems():
      processed[timestamp] = ','.join(data)
    return list(processed.iteritems())

