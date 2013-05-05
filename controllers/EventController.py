import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import images
from model.event import Event

import os

class EventController(webapp2.RequestHandler):

    @staticmethod
    def getTemplate(path):
        jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace('controllers','')))
        return jinja_environment.get_template(path)

    def get(self):
        events = getAllEvents(self)
        templateValues = {
            'events': events
        }

        template = EventController.getTemplate('templates/events.html')
        self.response.out.write(template.render(templateValues))

    class NewEventHandler(webapp2.RequestHandler):

        def get(self):
            template = EventController.getTemplate('templates/new_event.html')
            self.response.out.write(template.render({}))

        def post(self):
            event = Event()
            event.name = self.request.get("name")
            event.description = self.request.get("description")
            event.location = self.request.get("location")
            event.date = self.request.get("date")
            event.time = self.request.get("time")
            event.linkFacebook = self.request.get("facebook_link")
            event.eventTag = "default-tag"
            event.author = "default"

            if self.request.get("image"):
                event.image = db.Blob(images.resize(self.request.get("image"), 600))

            event.put()
            self.redirect("/events")

    class ShowEventHandler(webapp2.RequestHandler):

        def get(self, *args):
            event = getEvent(args[0])
            template = EventController.getTemplate('templates/show_event.html')
            self.response.out.write(template.render(event))

    class DeleteEventHandler(webapp2.RequestHandler):

        def get(self, *args):
            event = Event.get_by_id(long(args[0]))

            if event:
                event.delete()

            self.redirect('/events')

    class EditEventHandler(webapp2.RequestHandler):

        def get(self, ident):
            event = getEvent(ident)
            template = EventController.getTemplate('templates/edit_event.html')
            self.response.out.write(template.render(event))

        def post(self, ident):
            event = Event.get_by_id(long(ident))
            event.name = self.request.get("name")
            event.description = self.request.get("description")
            event.location = self.request.get("location")
            event.date = self.request.get("date")
            event.time = self.request.get("time")
            event.linkFacebook = self.request.get("facebook_link")
            event.eventTag = "default-tag"
            event.author = "default"

            if self.request.get("image"):
                event.image = db.Blob(images.resize(self.request.get("image"), 600))

            db.put(event)
            self.redirect("/events")

    class ImageHandler(webapp2.RequestHandler):

        def get(self, ident):
            event = Event.get_by_id(long(ident))

            if event.image:
                self.response.headers['Content-Type'] = 'image/*'
                self.response.out.write(event.image)


def getAllEvents(self):
    query = db.GqlQuery("SELECT * FROM Event")
    events = []

    for n in query:

        jsonEventInfo = {}
        jsonEventInfo['name'] = n.name
        jsonEventInfo['description'] = n.description
        jsonEventInfo['location'] = n.location
        jsonEventInfo['date'] = n.date
        jsonEventInfo['time'] = n.time
        jsonEventInfo['facebook_link'] = n.linkFacebook
        jsonEventInfo['image_key'] = n.imageKey
        jsonEventInfo['author'] = n.author
        currentUrl = self.request.url;

        jsonEventInfo['delete_link'] = currentUrl + '/delete/' + str(n.key().id())
        jsonEventInfo['edit_link'] = currentUrl + '/edit/' + str(n.key().id())
        jsonEventInfo['direct_link'] = currentUrl + '/' + str(n.key().id())
        events.append(jsonEventInfo)

    return events


def getEvent(ident):
    event = Event.get_by_id(long(ident))

    jsonEventInfo = {}
    jsonEventInfo['name'] = event.name
    jsonEventInfo['description'] = event.description
    jsonEventInfo['location'] = event.location
    jsonEventInfo['date'] = event.date
    jsonEventInfo['time'] = event.time
    jsonEventInfo['facebook_link'] = event.linkFacebook
    jsonEventInfo['image_key'] = event.imageKey
    jsonEventInfo['author'] = event.author
    jsonEventInfo['image_link'] = '/events/images/' + str(ident)

    event = jsonEventInfo
    return event
