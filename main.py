import webapp2
import jinja2
import os
import time
from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.api import users
from database import load
from app_models import make_User, User, Family, ANCESTORY_KEY_FAM, ANCESTORY_KEY_USR, Comment
import json


the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

families_query = Family.query(ancestor=ANCESTORY_KEY_FAM)
states = {}

for family in families_query:
    if family.state in states:
        if family.city not in states[family.state]:
            states[family.state].append(family.city)
    else:
        states[family.state] = [family.city]

states = json.dumps(states)


def get_current_user(current_page):
    google_user = users.get_current_user()
    if google_user:
        google_user_id = str(google_user.user_id())
        user = User.query(ancestor=ANCESTORY_KEY_USR).filter(User.user_id == google_user_id).get()
        if not user:
            user = make_User(google_user_id)

        return user
    else:
        current_page.redirect('/')


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


class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            self.response.write('Welcome, {}! (<a href="{}">sign out</a>)(<a href="{}">search</a>)'.format(nickname, logout_url, '/search'))
        else:
            login_url = users.create_login_url('/search')
            self.redirect(login_url)


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = get_current_user(self)
        if user:
            main_page_template = the_jinja_env.get_template('templates/main_page.html')
            self.response.write(main_page_template.render({'states':states}))

    def post(self):
        family_id = self.request.get('id')
        if family_id:
            self.redirect('/family?id=' + family_id)
        else:
            self.redirect('/search')


class FamilyPage(webapp2.RequestHandler):
    def get(self):
        user = get_current_user(self)
        if user:
            family_id = self.request.get('id')
            if family_id:
                family = ndb.Key(urlsafe=family_id).get()

                family_page_template = the_jinja_env.get_template('templates/family_page.html')
                ratings = json.loads(family.ratings)
                ratings = json.dumps(ratings)

                user_ratings = json.loads(user.ratings)
                user_family_ratings = [0, 0, 0, 0, 0]

                if str(family_id) in user_ratings:
                    user_family_ratings = user_ratings[str(family_id)]
                else:
                    user_ratings[str(family_id)] = [0, 0, 0, 0, 0]
                    user.user_ratings = json.dumps(user_ratings)
                    user.put()

                user_family_ratings = json.dumps(user_family_ratings)
                self.response.write(family_page_template.render({
                    'family_id': family_id,
                    'name': family.name,
                    'state': family.state,
                    'city': family.city,
                    'family_image': '/images/families/'+family.house_image,
                    'house_image': '/images/houses/'+family.house_image,
                    'ratings': ratings,
                    'user_ratings': user_family_ratings,
                    'comments': family.comments,
                }))
                return

            self.redirect('/search')


class Load(webapp2.RequestHandler):
    def get(self):
        load()

        families_query = Family.query(ancestor=ANCESTORY_KEY_FAM)
        states = {}

        for family in families_query:
            if family.state in states:
                if family.city not in states[family.state]:
                    states[family.state].append(family.city)
            else:
                states[family.state] = [family.city]

        states = json.dumps(states)

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

        time.sleep(2)
        self.redirect('/search')


class InputHandler(webapp2.RequestHandler):
    def post(self):
        input = self.request.get('input')
        data = {
            'response': False,
        }

        results = search.Index(name="item_autocomplete").search(
            "name:" + input
        )
        families = []
        if results:
            for result in results:
                family = ndb.Key(urlsafe=result.doc_id).get()
                if family:
                    families.append({
                        'name': family.name,
                        'id': family.key.urlsafe(),
                    })
        if len(families) > 0:
            data['response'] = families

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))


class UpdateHandler(webapp2.RequestHandler):
    def post(self):
        user = get_current_user(self)
        if user:
            row = self.request.get('row')
            star = self.request.get('star')
            family_id = self.request.get('family_id')
            if row and star and family_id:
                user_ratings = json.loads(user.ratings)
                family = ndb.Key(urlsafe=family_id).get()

                family_ratings = json.loads(family.ratings)
                if family_id in user_ratings:
                    previous_rating = user_ratings[family_id][int(row) - 1]
                    if previous_rating > 0:
                        family_ratings[int(row) - 1]['total_rating'] -= previous_rating
                        family_ratings[int(row) - 1]['total_rating'] += int(star)
                        user_ratings[family_id][int(row) - 1] = int(star)

                        user.ratings = json.dumps(user_ratings)
                        user.put()
                    else:
                        family_ratings[int(row) - 1]['total_rating'] += int(star)
                        family_ratings[int(row) - 1]['times_rated'] += 1
                        user_ratings[family_id][int(row) - 1] = int(star)

                        user.ratings = json.dumps(user_ratings)
                        user.put()
                else:
                    family_ratings[int(row) - 1]['total_rating'] += int(star)
                    family_ratings[int(row) - 1]['times_rated'] += 1

                    user_ratings[family_id] = [0, 0, 0, 0, 0]
                    user_ratings[family_id][int(row) - 1] = int(star)

                    user.ratings = json.dumps(user_ratings)
                    user.put()

                family.ratings = json.dumps(family_ratings)
                family.put()


class CommentHandler(webapp2.RequestHandler):
    def post(self):
        family_id = self.request.get('family_id')
        content = self.request.get('content')

        family = ndb.Key(urlsafe=family_id).get()
        if family:
            if len(content) > 0:
                new_comment = Comment(content=content)
                family.comments.insert(0, new_comment)
                family.put()


class GetData(webapp2.RequestHandler):
    def post(self):
        family_id = self.request.get('family_id')
        family = ndb.Key(urlsafe=family_id).get()
        if family:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(family.ratings))


app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/search', MainPage),
    ('/family', FamilyPage),
    ('/input', InputHandler),
    ('/update', UpdateHandler),
    ('/comment', CommentHandler),
    ('/load', Load),
    ('/get_data', GetData)
], debug=True)
