#!/usr/bin/python

import webapp2
from google.appengine.ext import db
from model.event import Event

import datetime
import json
import base64
import os
import logging
import re

class DataController(webapp2.RequestHandler):

    class GetEventData(webapp2.RequestHandler):

        def get(self, ident):
            event = Event.get_by_id(long(ident))
            self.response.headers['Content-Type'] = 'application/json'

            eventData = {
                "name": event.name,
                "description": event.description,
                "local": event.local,
                "date": event.date,
                "time": event.time,
                "facebook_link": event.linkFacebook,
                "image": base64.b64encode(str(event.image))
            }
            jsonEventData = json.dumps(eventData)
            self.response.write(jsonEventData)

    class GetAllEventsData(webapp2.RequestHandler):

        def get(self):
            self.response.headers['Content-Type'] = 'application/json'
            query = db.GqlQuery("SELECT * FROM Event")
            eventsData = []

            for event in query:
                eventData = {
                    "id": event.key().id(),
                    "name": event.name,
                    "description": event.description,
                    "local": event.local,
                    "date": event.date,
                    "time": event.time,
                    "facebook_link": event.linkFacebook,
                    "image": base64.b64encode(str(event.image))
                }

                eventsData.append(eventData)

            jsonEventsData = json.dumps(eventsData)

            self.response.write(jsonEventsData)
