from google.appengine.ext import db


class Event(db.Model):
    name = db.StringProperty()
    description = db.TextProperty()
    linkFacebook = db.LinkProperty()
    location = db.StringProperty()
    date = db.StringProperty()
    time = db.StringProperty()
    imageKey = db.StringProperty()
    image = db.BlobProperty()
    eventTag = db.StringProperty()
    author = db.StringProperty()

    @staticmethod
    def deleteEvent(event_name):
      events = db.GqlQuery("SELECT * from Event")

      for e in events:
        if e.name == event_name:
          e.delete()
          break
