from google.appengine.ext import db
from google.appengine.api import users

class Votes(db.Model):
    upVotes = db.IntegerProperty(default = 0)
    downVotes = db.IntegerProperty(default = 0)
    mealID = db.StringProperty()
