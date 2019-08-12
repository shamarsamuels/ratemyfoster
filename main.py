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

families = Family.query()
families_list = []
for family in families:
    families_list.append({'name': family.name, 'id': family.key.id()})
families_list = json.dumps(families_list)

class MainPage(webapp2.RequestHandler):
    def get(self):
        main_page_template = the_jinja_env.get_template('templates/main_page.html')
        self.response.write(main_page_template.render({'families': families_list}))

    def post(self):
        family_id = self.request.get('id')
        if family_id:
            self.redirect('/family?id=' + family_id)
        else:
            self.redirect('/')


class FamilyPage(webapp2.RequestHandler):
    def get(self):
        family_id = self.request.get('id')
        if family_id:
            if family_id.isdigit():
                family_id = int(family_id)
                print(family_id)
                return
        self.redirect('/')


class Load(webapp2.RequestHandler):
    def get(self):
        load()

        families = Family.query()
        families_list = []
        for family in families:
            families_list.append({'name': family.name, 'id': family.key.id()})
        families_list = json.dumps(families_list)

        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/load', Load),
    ('/family', FamilyPage)
], debug=True)
