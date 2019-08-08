from app_models import Family

def load():
    Family(name='Browns',city='Brooklyn',state='New York').put()
    Family(name='Blacks',city='Brooklyn',state='New York').put()