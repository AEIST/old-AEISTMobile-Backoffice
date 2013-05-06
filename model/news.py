from google.appengine.ext import db


class News(db.Model):
    title = db.StringProperty()
    short_description = db.TextProperty()
    description = db.TextProperty()
    created_at = db.StringProperty()
    imageKey = db.StringProperty()
    image = db.BlobProperty()


