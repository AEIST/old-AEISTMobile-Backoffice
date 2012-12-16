#!/usr/bin/python

from google.appengine.ext import webapp
from google.appengine.ext import db
from model.event import Evento

import json
import logging

class EventController(webapp.RequestHandler):

	def deleteEvent(self, eventName):
		self.response.out.write('TODO: ' + eventName + "\n");

		query = db.GqlQuery("SELECT * "
							"FROM Evento "
							"WHERE nome = :1", eventName)
		event = query.get()

		if not event:
			## TODO: redirect to home page. Javascript popup with error message
			self.response.out.write('error: no such event')
		else :
			event.delete()
			# TODO: redirect to home page. Javascript popup saying all went well
			self.response.out.write('Event deleted with success')


	def updateEvent(self, eventName, updates):
		self.response.out.write('TODO');

	def get(self, *args):

		self.response.headers['Content-Type'] = 'text/plain'
		requestType = self.request.get('type')

		if requestType == 'delete':
			event_name = self.request.get('name')
			self.deleteEvent(event_name)

		else :
			if requestType == 'update':
				event_name = self.request.get('name')
				self.updateEvent(event_name)

	
		