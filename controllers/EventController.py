#!/usr/bin/python

import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import images
from model.event import Event

import datetime
import json
import os
import logging
import re

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
            event.local = self.request.get("local")
            event.date = self.request.get("date")
            event.time = self.request.get("time")
            event.linkFacebook = self.request.get("facebook_link")
            event.eventTag = "default-tag"
            event.author = "default"

            if self.request.get("image"):
                event.image = db.Blob(images.resize(self.request.get("image"), 300))

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
            event.nome = self.request.get("name")
            event.descricao = self.request.get("description")
            event.local = self.request.get("local")
            event.date = self.request.get("date")
            event.time = self.request.get("time")
            event.link_facebook = self.request.get("facebook_link")
            event.eventTag = "default-tag"
            event.author = "default"

            if self.request.get("image"):
                event.image = db.Blob(images.resize(self.request.get("image"), 300))

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
        jsonEventInfo['name'] = str(n.name)
        jsonEventInfo['description'] = str(n.description)
        jsonEventInfo['local'] = str(n.local)
        jsonEventInfo['date'] = str(n.date)
        jsonEventInfo['time'] = str(n.time)
        jsonEventInfo['facebook_link'] = str(n.linkFacebook)
        jsonEventInfo['image_key'] = str(n.imageKey)
        jsonEventInfo['author'] = str(n.author)
        currentUrl = self.request.url;

        # if " " in jsonEventInfo['name']:
        #     jsonEventInfo['name'] = re.sub(r"\s","_", jsonEventInfo['name'])

        jsonEventInfo['delete_link'] = currentUrl + '/delete/' + str(n.key().id())
        jsonEventInfo['edit_link'] = currentUrl + '/edit/' + str(n.key().id())
        jsonEventInfo['direct_link'] = currentUrl + '/' + str(n.key().id())
        events.append(jsonEventInfo)

    return events


def getEvent(ident):
    event = Event.get_by_id(long(ident))

    jsonEventInfo = {}
    jsonEventInfo['name'] = str(event.name)
    jsonEventInfo['description'] = str(event.description)
    jsonEventInfo['local'] = str(event.local)
    jsonEventInfo['date'] = str(event.date)
    jsonEventInfo['time'] = str(event.time)
    jsonEventInfo['facebook_link'] = str(event.linkFacebook)
    jsonEventInfo['image_key'] = str(event.imageKey)
    jsonEventInfo['author'] = str(event.author)
    jsonEventInfo['image_link'] = '/events/images/' + str(ident)

    # if " " in jsonEventInfo['name']:
    #     jsonEventInfo['name'] = re.sub(r"\s","_",jsonEventInfo['name'])

    event = jsonEventInfo
    return event
