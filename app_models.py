from google.appengine.ext import ndb
from google.appengine.api import search 

class Family(ndb.Model):
    name = ndb.StringProperty(required=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())
    city = ndb.StringProperty(required=True)
    state = ndb.StringProperty(required=True)
    rating = ndb.IntegerProperty(default=100)
