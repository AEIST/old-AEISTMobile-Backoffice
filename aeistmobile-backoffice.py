#!/usr/bin/python

import logging
import os
import json
import re

import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import users


# from events.web_services import GetAllEventsNames
# from events.web_services import GetEventInformation
# from events.web_services import ShowAllEvents

from controllers.EventController import EventController
from controllers.NewsController import NewsController
from controllers.DataController import DataController


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def getAllEvents(self):
      query = db.GqlQuery("SELECT * FROM Event")
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

class Logout(webapp2.RequestHandler):
    
    def get(self):
        self.redirect(users.create_logout_url("/"))


class MainPage(webapp2.RequestHandler):

    def get(self):
      template = jinja_environment.get_template('templates/index.html')
      self.response.out.write(template.render({}))

routes = [
          ('/', MainPage),
          ('/logout', Logout),
          ('/events', EventController),
          ('/events/new', EventController.NewEventHandler),
          (r'/events/(\d+)', EventController.ShowEventHandler),
          (r'/events/delete/(\d+)', EventController.DeleteEventHandler),
          (r'/events/edit/(\d+)', EventController.EditEventHandler),
          (r'/events/images/(\d+)', EventController.ImageHandler),
          ('/news', NewsController),
          ('/news/new', NewsController.NewNewsHandler),
          (r'/news/(\d+)', NewsController.ShowNewsHandler),
          (r'/news/delete/(\d+)', NewsController.DeleteNewsHandler),
          (r'/news/edit/(\d+)', NewsController.EditNewsHandler),
          (r'/news/images/(\d+)', NewsController.ImageHandler)
          ]

app = webapp2.WSGIApplication(routes=routes, debug=True)
