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
states = {}

for family in families:
    if family.state in states:
        if not family.city in states[family.state]:
            states[family.state].append(family.city)
    else:
        states[family.state] = [family.city]

states = json.dumps(states)

class MainPage(webapp2.RequestHandler):
    def get(self):
        main_page_template = the_jinja_env.get_template('templates/main_page.html')
        self.response.write(main_page_template.render({'states':states}))

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
                family_page_template = the_jinja_env.get_template('templates/family_page.html')
                self.response.write(family_page_template.render({'name':'Samuels'}))
                return

        self.redirect('/')


class Load(webapp2.RequestHandler):
    def get(self):
        load()

        families = Family.query()
        states = {}

        for family in families:
            if family.state in states:
                if not family.city in states[family.state]:
                    states[family.state].append(family.city)
            else:
                states[family.state] = [family.city]

        states = json.dumps(states)

        self.redirect('/')

class InputHandler(webapp2.RequestHandler):
    def post(self):
        input = self.request.get('input')
        # Create an array
        data = {
            'response':False,
        }

        families_query = Family.query()
        families_search = families_query.filter(Family.name_lower == 'brown').fetch()
        families = []

        for family in families_search:
            families.append(family)

        data['response'] = families

        # Output the JSON
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/load', Load),
    ('/family', FamilyPage),
    ('/input', InputHandler)
], debug=True)
