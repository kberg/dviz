import datastore

def test_add_get():
  d = datastore.Datastore()
  d.add('temp', 42, 123)
  d.add('temp', 45, 125)
  d.add('temp', 41, 129)
  d.add('temp2', 41, 999)

  print 'temp', d.get('temp')
  print '--'
  print 'temp2', d.get('temp2')

def test_getmany():
  d = datastore.Datastore()
  data = d.getmany(['94303_temp', '90034_temp', 'taipei_temp'])
  for d in data:
    print '\t'.join([str(dd) for dd in d])


test_getmany()
