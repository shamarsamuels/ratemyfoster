import webapp2
import jinja2
import os
import time
from google.appengine.ext import ndb
from database import load
from app_models import Family
import json


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        main_page_template = the_jinja_env.get_template('templates/main_page.html')
        families = Family.query()
        families_list = []
        for family in families:
            families_list.append({'name': family.name})

        families_list = json.dumps(families_list)
        print(families_list)
        self.response.write(main_page_template.render({'families': families_list}))



class Load(webapp2.RequestHandler):
    def get(self):
        load()
        self.redirect('/')

class Load(webapp2.RequestHandler):
    def get(self):
        load()
        self.response.write('Loaded')
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/load', Load)
], debug=True)