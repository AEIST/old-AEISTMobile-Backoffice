'''
Created on Oct 29, 2012

@author: joaovasques
'''
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import webapp
import datetime
import logging


class Evento(db.Model):
    nome = db.StringProperty()
    descricao = db.TextProperty()
    link_facebook = db.LinkProperty()
    local = db.StringProperty()
    date = db.StringProperty()
    time = db.StringProperty()
    imagem_key = db.StringProperty()
    image = db.BlobProperty()
    eventTag = db.StringProperty()
    author = db.StringProperty()
    #time = db.DateTimeProperty()

    @staticmethod
    def deleteEvent(event_name):
      events = db.GqlQuery("SELECT * from Evento")

      for e in events:
        if e.name == event_name:
          e.delete()
          break