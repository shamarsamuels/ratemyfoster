import webapp2
import jinja2
import os
import time
from google.appengine.ext import ndb
from google.appengine.api import search
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

families_query = Family.query()

def tokenize_autocomplete(phrase):
    a = []
    for i in range(0, len(phrase) + 1):
        a.append(phrase[0:i])

    return a

index = search.Index(name='item_autocomplete')
for item in families_query:  # item = ndb.model
    doc_id = item.key.urlsafe()
    name = ','.join(tokenize_autocomplete(item.name))
    state = item.state
    document = search.Document(
        doc_id=doc_id,
        fields=[
            search.TextField(name='name', value=name),
            search.TextField(name='state', value=state)
        ])
    index.put(document)

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
                family = Family.get_by_id(family_id)
                family_page_template = the_jinja_env.get_template('templates/family_page.html')
                self.response.write(family_page_template.render({'name':family.name, 'state':family.state, 'city':family.city, 'image':'/images/families/'+ family.image}))
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

        '''
        families_query = Family.query()
        families_filter = families_query.filter(Family.name_lower >= 'ba').fetch()
        families = []
        
        for family in families_filter:
            print(family.name)
        '''

        
        results = search.Index(name="item_autocomplete").search(
            "name:" + input
        )
        #result = Family.
        families = []
        if results:
            for result in results:
                family = ndb.Key(urlsafe=result.doc_id).get()
                if family:
                    families.append({
                        'name':family.name,
                        'id':family.key.id(),
                    })
        #print(results[0].doc_id.get())
        

        '''
        results = ndb.gql("SELECT * FROM Family WHERE name_lower >= 'b' AND name_lower < 'b*'").fetch()
        
        if results:
            for i in results:
                print(i)
        else:
            print('No Return')
        '''
        
        '''
        families_search = families_query.fetch()

        for family in families_search:
            if family.name_lower[0:len(input)] == input:
                families.append({
                    "name":family.name,
                    "id":family.key.id()
                })

        if len(families) > 0:
            data['response'] = families
        
        '''

        if len(families) > 0:
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
