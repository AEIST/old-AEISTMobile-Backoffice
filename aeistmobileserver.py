#!/usr/bin/python

import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

import json

from events.operations import CreateNewEventController

from events.web_services import GetAllEventsNames
from events.web_services import GetEventInformation
from events.web_services import ShowAllEvents

from controllers.EventController import EventController


def getAllEvents():

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
          events.append(json_event_info)
            
      return events                

class MainPage(webapp.RequestHandler):
    
    
    def get(self):

      events = getAllEvents()

      templateValues = {
            'events': events
      }

      path = os.path.join(os.path.dirname(__file__), 'Resources/html/index.html')
      self.response.out.write(template.render(path, templateValues))

           
application = webapp.WSGIApplication([
                                      ('/', MainPage),
                                      ('/delete-event',EventController),
                                      ('/novoevento', CreateNewEventController),
                                      ('/getalleventsnames',GetAllEventsNames),
                                      ('/showallevents',ShowAllEvents),
                                      ('/geteventinfo',GetEventInformation),
                                      ]
                                      ,debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
