import datastore

d = datastore.Datastore()
d.add('temp', 42, 123)
d.add('temp', 45, 125)
d.add('temp', 41, 129)
d.add('temp2', 41, 999)

print 'temp', d.get('temp')
print '--'
print 'temp2', d.get('temp2')

