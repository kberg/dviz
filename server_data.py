import web
import datastore

class Data:
  def GET(self, names):
    d = datastore.Datastore()
    names = names.split(',')
    if len(names) == 0:
      return ''
    if len(names) == 1:
      data = d.get(names[0])
      data = ['\t'.join([str(dd) for dd in d]) for d in data]
      return '\n'.join(data)



    data = d.getmany(names)
    data = ['\t'.join([str(dd) for dd in d]) for d in data]
    return '\n'.join(data)

