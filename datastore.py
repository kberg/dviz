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
      list of (int timestamp, data name, int value) tuples.
    """
    # TODO(rob): write me.

