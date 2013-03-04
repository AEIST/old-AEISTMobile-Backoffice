#!/usr/bin/python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import images
from model.event import Evento

import datetime
import json
import os
import logging
import re

class EventController(webapp.RequestHandler):

    def get(self):

        events = getAllEvents(self)

        templateValues = {
            'events': events
        }

        path = os.path.join(os.path.dirname(__file__), '../templates/events.html')
        self.response.out.write(template.render(path, templateValues))

    class NewEventHandler(webapp.RequestHandler):
        def get(self):
            self.response.out.write(template.render('templates/new_event.html', {}))

        def post(self):
            event_name = self.request.get("name")
            description = self.request.get("description")
            local = self.request.get("local")
            date = self.request.get("date")
            time = self.request.get("time")
            facebook_link = self.request.get("facebook_link")
            image = self.request.get("image")
            creationDate = datetime.datetime.now()


            event = Evento()
            event.nome = event_name
            event.descricao = description
            event.local = local
            event.date = date
            event.time = time
            event.link_facebook = facebook_link
            event.eventTag = "default-tag"
            #event.time = creationDate
            event.author = "default"

            # if image:
            #     event.image = db.Blob(images.resize(image, 300))
                
            event.put()
            
            self.redirect("/events")

    class ShowEventHandler(webapp.RequestHandler):
        def get(self, *args):
        
            event_id = args[0]
            event = getEvent(event_id)

            self.response.out.write(template.render('templates/show_event.html', event))

    class DeleteEventHandler(webapp.RequestHandler):
        def get(self, *args):

            event_id = args[0]

            event = Evento.get_by_id(long(event_id))

            if event:
                event.delete()

            self.redirect('/events')

    class EditEventHandler(webapp.RequestHandler):

        def get(self, ident):
            event_id = ident

            event = getEvent(event_id)

            self.response.out.write(template.render('templates/edit_event.html', event))

        def post(self, ident):

            event_id = ident

            eventName = self.request.get("name")
            description = self.request.get("description")
            local = self.request.get("local")
            date = self.request.get("date")
            time = self.request.get("time")
            facebookLink = self.request.get("facebook_link")
            image = self.request.get("image")
            # creationDate = datetime.datetime.now()

            event = Evento.get_by_id(long(event_id))
            event.nome = eventName
            event.descricao = description
            event.local = local
            event.date = date
            event.time = time
            event.link_facebook = facebookLink
            event.eventTag = "default-tag"
            # event.time = creationDate
            event.author = "default"

            if image:
                event.image = db.Blob(image)

            db.put(event)
            
            self.redirect("/events")

    class ImageHandler(webapp.RequestHandler):
    
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
        
        json_event_info = {}

        ident = n.key().id()
        name = n.nome
        des = n.descricao
        local = n.local
        date = n.date
        time = n.time
        link = n.link_facebook
        image_key = n.imagem_key
        # time = n.time
        author = n.author

        json_event_info['name'] = str(name)
        json_event_info['description'] = str(des)
        json_event_info['local'] = str(local)
        json_event_info['date'] = str(date)
        json_event_info['time'] = str(time)
        json_event_info['facebook_link'] = str(link)
        json_event_info['image_key'] = str(image_key)
        # json_event_info['time'] = str(time)
        json_event_info['author'] = str(author)
        currentUrl = self.request.url;

        if " " in name:
            name = re.sub(r"\s","_",name)

        json_event_info['delete_link'] = currentUrl + '/delete/' + str(ident)
        json_event_info['edit_link'] = currentUrl + '/edit/' + str(ident)
        json_event_info['direct_link'] = currentUrl + '/' + str(ident)
        events.append(json_event_info)

    return events


def getEvent(ident):

    event = Evento.get_by_id(long(ident))
        
    json_event_info = {}

    name = event.nome
    des = event.descricao
    local = event.local
    date = event.date
    time = event.time
    link = event.link_facebook
    image_key = event.imagem_key
    # time = event.time
    author = event.author

    json_event_info['name'] = str(name)
    json_event_info['description'] = str(des)
    json_event_info['local'] = str(local)
    json_event_info['date'] = str(date)
    json_event_info['time'] = str(time)
    json_event_info['facebook_link'] = str(link)
    json_event_info['image_key'] = str(image_key)
    # json_event_info['time'] = str(time)
    json_event_info['author'] = str(author)
    json_event_info['image_link'] = '/events/images/' + str(ident)

    if " " in name:
        name = re.sub(r"\s","_",name)

    event = json_event_info

    return event

