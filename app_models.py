from google.appengine.ext import ndb

class Family(ndb.Model):
    name = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    state = ndb.StringProperty(required=True)
    rating = ndb.IntegerProperty(default = 100)