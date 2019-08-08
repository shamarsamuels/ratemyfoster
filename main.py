import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from database import load

load()

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        main_page_template = the_jinja_env.get_template('templates/main_page.html')
        self.response.write(main_page_template.render())


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)