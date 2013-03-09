#!/usr/bin/python

import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import images
from model.event import Evento

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

            event = Evento()
            event.nome = self.request.get("name")
            event.descricao = self.request.get("description")
            event.local = self.request.get("local")
            event.date = self.request.get("date")
            event.time = self.request.get("time")
            event.link_facebook = self.request.get("facebook_link")
            event.eventTag = "default-tag"
            event.author = "default"

            # if self.request.get("image"):
            #     event.image = db.Blob(images.resize(self.request.get("image"), 300))

            event.put()

            self.redirect("/events")

    class ShowEventHandler(webapp2.RequestHandler):
        def get(self, *args):

            event_id = args[0]
            event = getEvent(event_id)

            template = EventController.getTemplate('templates/show_event.html')
            self.response.out.write(template.render({}))

    class DeleteEventHandler(webapp2.RequestHandler):
        def get(self, *args):

            event_id = args[0]
            event = Evento.get_by_id(long(event_id))

            if event:
                event.delete()

            self.redirect('/events')

    class EditEventHandler(webapp2.RequestHandler):

        def get(self, ident):

            event_id = ident
            event = getEvent(event_id)
            template = EventController.getTemplate('templates/edit_event.html')
            self.response.out.write(template.render({}))

        def post(self, ident):

            event_id = ident
            event = Evento.get_by_id(long(ident))
            event.nome = self.request.get("name")
            event.descricao = self.request.get("description")
            event.local = self.request.get("local")
            event.date = self.request.get("date")
            event.time = self.request.get("time")
            event.link_facebook = self.request.get("facebook_link")
            event.eventTag = "default-tag"
            event.author = "default"

            # if image:
            #     event.image = db.Blob(self.request.get("image"))

            db.put(event)
            self.redirect("/events")

    class ImageHandler(webapp2.RequestHandler):

        def get(self, ident):
            event = Evento.get_by_id(long(ident))

            if event.image:
                self.response.headers['Content-Type'] = 'image/*'
                self.response.out.write(event.image)


def getAllEvents(self):

    query = db.GqlQuery("SELECT * "
                        "FROM Evento")
    events = []

    for n in query:

        jsonEventInfo = {}
        jsonEventInfo['name'] = str(n.nome)
        jsonEventInfo['description'] = str(n.descricao)
        jsonEventInfo['local'] = str(n.local)
        jsonEventInfo['date'] = str(n.date)
        jsonEventInfo['time'] = str(n.time)
        jsonEventInfo['facebook_link'] = str(n.link_facebook)
        jsonEventInfo['image_key'] = str(n.imagem_key)
        jsonEventInfo['author'] = str(n.author)
        currentUrl = self.request.url;

        if " " in jsonEventInfo['name']:
            jsonEventInfo['name'] = re.sub(r"\s","_", jsonEventInfo['name'])

        jsonEventInfo['delete_link'] = currentUrl + '/delete/' + str(n.key().id())
        jsonEventInfo['edit_link'] = currentUrl + '/edit/' + str(n.key().id())
        jsonEventInfo['direct_link'] = currentUrl + '/' + str(n.key().id())
        events.append(jsonEventInfo)

    return events


def getEvent(ident):

    event = Evento.get_by_id(long(ident))

    jsonEventInfo = {}
    jsonEventInfo['name'] = str(event.nome)
    jsonEventInfo['description'] = str(event.descricao)
    jsonEventInfo['local'] = str(event.local)
    jsonEventInfo['date'] = str(event.date)
    jsonEventInfo['time'] = str(event.time)
    jsonEventInfo['facebook_link'] = str(event.link_facebook)
    jsonEventInfo['image_key'] = str(event.imagem_key)
    jsonEventInfo['author'] = str(event.author)
    jsonEventInfo['image_link'] = '/events/images/' + str(ident)

    if " " in jsonEventInfo['name']:
        jsonEventInfo['name'] = re.sub(r"\s","_",jsonEventInfo['name'])

    event = jsonEventInfo

    return event

