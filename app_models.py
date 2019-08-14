from google.appengine.ext import ndb
from google.appengine.api import search 
import os, random
import json

class Family(ndb.Model):
    name = ndb.StringProperty(required=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())
    city = ndb.StringProperty(required=True)
    state = ndb.StringProperty(required=True)
    image = ndb.StringProperty(required=False)
    ratings = ndb.StringProperty(required=False)

def make_Family(name, city, state):
    new_family = Family(name=name, city=city, state=state)
    new_family.image = str(random.randint(1,61))
    new_family.ratings = json.dumps({
        'parenting':5,
        'cleanliness':5,
        'environment':5,
        'schools':5,
        'experience':5,
    })
    new_family.put()
