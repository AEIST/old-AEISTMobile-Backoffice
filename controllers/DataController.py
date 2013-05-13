#!/usr/bin/python

import webapp2
from google.appengine.ext import db
from model.event import Event
from model.news import News

import json
import base64
from datetime import datetime

class DataController(webapp2.RequestHandler):

    class GetEventData(webapp2.RequestHandler):

        def get(self, ident):
            event = Event.get_by_id(long(ident))
            self.response.headers['Content-Type'] = 'application/json'

            eventData = {
                "name": event.name,
                "description": event.description,
                "location": event.location,
                "date": event.date.strftime('%d-%m-%Y'),
                "time": event.time,
                "facebook_link": event.linkFacebook,
                "image": base64.b64encode(str(event.image))
            }
            jsonEventData = json.dumps(eventData)
            self.response.write(jsonEventData)

    class GetAllEventsData(webapp2.RequestHandler):

        def get(self):
            self.response.headers['Content-Type'] = 'application/json'
            query = Event.all().order("-date")
            eventsData = []

            for event in query:
                eventData = {
                    "id": event.key().id(),
                    "name": event.name,
                    "description": event.description,
                    "location": event.location,
                    "date": event.date.strftime('%d-%m-%Y'),
                    "time": event.time,
                    "facebook_link": event.linkFacebook,
                    "image": base64.b64encode(str(event.image))
                }

                eventsData.append(eventData)

            jsonEventsData = json.dumps(eventsData)

            self.response.write(jsonEventsData)
            
    class GetNextEventsData(webapp2.RequestHandler):
        
        def get(self):
            self.response.headers['Content-Type'] = 'application/json'
            query = Event.all().order("date").filter("date >=", datetime.now().date())
            eventsData = []

            for event in query:
                eventData = {
                    "id": event.key().id(),
                    "name": event.name,
                    "description": event.description,
                    "location": event.location,
                    "date": event.date.strftime('%d-%m-%Y'),
                    "time": event.time,
                    "facebook_link": event.linkFacebook,
                    "image": base64.b64encode(str(event.image))
                }

                eventsData.append(eventData)

            jsonEventsData = json.dumps(eventsData)

            self.response.write(jsonEventsData)

    class GetNewsData(webapp2.RequestHandler):

        def get(self, ident):
            news = News.get_by_id(long(ident))
            self.response.headers['Content-Type'] = 'application/json'

            data = {
                "title": news.title,
                "short_description": news.short_description,
                "description": news.description,
                "created_at": news.created_at.strftime('%d-%m-%Y'),
                "image": base64.b64encode(str(news.image))
            }
            
            jsonNewsData = json.dumps(data)
            self.response.write(jsonNewsData)

    class GetAllNewsData(webapp2.RequestHandler):

        def get(self):
            self.response.headers['Content-Type'] = 'application/json'
            query = News.all().order("-created_at")
            newsData = []

            for news in query:
                data = {
                    "id": news.key().id(),
                    "title": news.title,
                    "short_description": news.short_description,
                    "description": news.description,
                    "created_at": news.created_at.strftime('%d-%m-%Y'),
                    "image": base64.b64encode(str(news.image))
                }

                newsData.append(data)

            jsonEventsData = json.dumps(newsData)

            self.response.write(jsonEventsData)
