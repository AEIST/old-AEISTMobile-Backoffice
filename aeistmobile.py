#!/usr/bin/python

import logging
import os
import json
import re

import webapp2
import jinja2
from google.appengine.ext import db


from events.operations import CreateNewEventController

from events.web_services import GetAllEventsNames
from events.web_services import GetEventInformation
from events.web_services import ShowAllEvents

from controllers.EventController import EventController
from controllers.DataController import DataController


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def getAllEvents(self):

      query = db.GqlQuery("SELECT * "
                            "FROM Evento")
      events = []

      for n in query:

          jsonEventInfo = {}
          jsonEventInfo['name'] = str(n.nome)
          jsonEventInfo['description'] = str(n.descricao)
          jsonEventInfo['facebook_link'] = str(n.link_facebook)
          jsonEventInfo['image_key'] = str(n.imagem_key)
          jsonEventInfo['time'] = str(n.time)
          jsonEventInfo['author'] = str(n.author)

          if " " in name:
            name = re.sub(r"\s","_",name)

          jsonEventInfo['deleteLink'] = self.request.url; + 'delete-event?name=' + name+"&type=delete"
          jsonEventInfo['updateLink'] = ""
          events.append(jsonEventInfo)

      return events



class MainPage(webapp2.RequestHandler):

    def get(self):
      template = jinja_environment.get_template('templates/index.html')
      self.response.out.write(template.render({}))


routes = [
          ('/', MainPage),
          ('/events', EventController),
          ('/events/new', EventController.NewEventHandler),
          (r'/events/(\d+)', EventController.ShowEventHandler),
          (r'/events/delete/(\d+)', EventController.DeleteEventHandler),
          (r'/events/edit/(\d+)', EventController.EditEventHandler),
          (r'/events/images/(\d+)', EventController.ImageHandler),
          (r'/data/events/(\d+)', DataController.GetEventData),
          (r'/data/events', DataController.GetAllEventsData),
          ('/delete-event',EventController),
          ('/getalleventsnames',GetAllEventsNames),
          ('/showallevents',ShowAllEvents),
          ]

app = webapp2.WSGIApplication(routes=routes, debug=True)
