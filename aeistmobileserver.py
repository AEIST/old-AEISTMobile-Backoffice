#!/usr/bin/python

import logging
import os
import json
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db


from events.operations import CreateNewEventController

from events.web_services import GetAllEventsNames
from events.web_services import GetEventInformation
from events.web_services import ShowAllEvents

from controllers.EventController import EventController
from controllers.DataController import DataController


def getAllEvents(self):

      query = db.GqlQuery("SELECT * "
                            "FROM Evento")      
      events = []
                
      for n in query:
            
          json_event_info = {}
            
          name = n.nome
          des = n.descricao
          link = n.link_facebook
          image_key = n.imagem_key
          time = n.time
          author = n.author
            
          json_event_info['name'] = str(name)
          json_event_info['description'] = str(des)
          json_event_info['facebook_link'] = str(link)
          json_event_info['image_key'] = str(image_key)
          json_event_info['time'] = str(time)
          json_event_info['author'] = str(author)
          currentUrl = self.request.url;

          if " " in name:
            name = re.sub(r"\s","_",name)

          json_event_info['deleteLink'] = currentUrl + 'delete-event?name=' + name+"&type=delete"
          json_event_info['updateLink'] = ""
          events.append(json_event_info)
            
      return events



class MainPage(webapp.RequestHandler):
    
    def get(self):

      path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
      self.response.out.write(template.render(path, {}))


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
    

           
application = webapp.WSGIApplication(routes=routes,debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
