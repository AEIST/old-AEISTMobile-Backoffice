'''
Created on Oct 29, 2012

@author: joaovasques
'''

import logging
from model.event import Evento
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import webapp
import datetime

image_blob_key = "" 

class CreateNewEventController(webapp.RequestHandler):
    
    # Present HTML form page
    def get(self):
        self.response.out.write(template.render("templates/novoevento.html",{}))

    # Gets information from the from and creates the new event
    def post(self, *args):
           
        eventName = self.request.get("eventName")
        description = self.request.get("description")
        facebookLink = self.request.get("facebookLink")
        image = self.request.get("image")
        creationDate = datetime.datetime.now()


        event = Evento()
        event.nome = eventName
        event.descricao = description
        event.link_facebook = facebookLink
        event.eventTag = "default-tag"
        event.time = creationDate
        event.author = "default"
        event.image = db.Blob(image)
        event.put()
        
        self.redirect("/events")
