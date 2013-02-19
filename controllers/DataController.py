#!/usr/bin/python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from model.event import Evento

import datetime
import json
import base64
import os
import logging
import re

class DataController(webapp.RequestHandler):

    class GetEventData(webapp.RequestHandler):

        def get(self, ident):
            event = Evento.get_by_id(long(ident))

            self.response.headers['Content-Type'] = 'application/json'

            event_data = {
                "name": event.nome,
                "description": event.descricao,
                "facebook_link": event.link_facebook,
                "image": base64.b64encode(str(event.image))
            }

            json_event_data = json.dumps(event_data)

            self.response.write(json_event_data)

    class GetAllEventsData(webapp.RequestHandler):

        def get(self):
            self.response.headers['Content-Type'] = 'application/json'
            
            query = db.GqlQuery("SELECT * FROM Evento")

            events_data = []

            for event in query:
                event_data = {
                    "name": event.nome,
                    "description": event.descricao,
                    "facebook_link": event.link_facebook,
                    "image": base64.b64encode(str(event.image))
                }

                events_data.append(event_data)

            json_events_data = json.dumps(events_data)

            self.response.write(json_events_data)