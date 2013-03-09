'''
Created on Oct 29, 2012

@author: joaovasques
'''

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
import json
import base64
import os
from protorpc import messages
from model.event import Event

class EventInformation(messages.Message):
    nome = messages.StringField(1)
    descricao = messages.StringField(2)
    link_facebook = messages.StringField(3)
    image_key = messages.StringField(5)
    eventTag = messages.StringField(4)
    image_base_64 = messages.StringField(6)

'''
Gets information about a specific event given key (name)

Information (JSON object) -> EventInformation
'''
class GetEventInformation(webapp.RequestHandler):

    def get(self, *args):
        eventName = str(self.request.get_all("name")[0]).replace("_", " ")

        self.response.headers['Content-Type'] = 'application/json'
        query = db.GqlQuery("SELECT * FROM Event")
        event = Event()
        eventInfo = {}

        for event in query:
            e = event

            if e.name == eventName:
                eventInfo['name'] = str(e.name)
                eventInfo['description'] = str(e.description)
                eventInfo['facebook_link'] = str(e.linkFacebook)
                eventInfo['author'] = e.author
                eventInfo['eventTag'] = e.eventTag
                eventInfo['image'] = base64.b64encode(str(e.image))
                #TODO: put binary into string -> base64 -> put into json array
                break

        json_eventInfo = json.dumps(eventInfo)
        self.response.out.write(json_eventInfo)


'''
Gets a list (JSON array) with the names of all events
'''
class GetAllEventsNames(webapp.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        query = db.GqlQuery("SELECT * FROM Event")
        events = []

        for n in query:
            jsonEventInfo = {}
            jsonEventInfo['name'] = n.name
            events.append(jsonEventInfo)

        r = {}
        r['events_names'] = events
        r = json.dumps(r)
        self.response.out.write(r)

'''
Returns a list (JSON array) with information about all events
'''
class ShowAllEvents(webapp.RequestHandler):

    def get(self, *args):
        self.response.headers['Content-Type'] = 'application/json'
        query = db.GqlQuery("SELECT * FROM Event")
        events = []

        for n in query:
            jsonEventInfo = {}
            jsonEventInfo['name'] = str(n.name)
            jsonEventInfo['description'] = str(n.description)
            jsonEventInfo['facebook_link'] = str(n.linkFacebook)
            jsonEventInfo['image_key'] = str(n.imageKey)
            events.append(jsonEventInfo)

        response = json.dumps(events)
        self.response.out.write(response)
