#!/usr/bin/python

from google.appengine.ext import webapp
from google.appengine.ext import db
from model.event import Evento

import json
import logging
import re

class EventController(webapp.RequestHandler):

	def deleteEvent(self, eventName):
		query = db.GqlQuery("SELECT * "
							"FROM Evento "
							"WHERE nome = :1", eventName)
		event = query.get()

		if not event:
			# TODO: Javascript popup with error message
			self.response.out.write('Info: no such event')
			values = {}
			values['eventDeleted'] = 'success';
			self.redirect('/')
		else :
			event.delete()
			# TODO: Javascript popup saying all went well
			self.response.out.write('Event deleted with success')
			self.redirect('/')			


	def updateEvent(self, eventName, updates):
		self.response.out.write('TODO');

	def get(self, *args):

		self.response.headers['Content-Type'] = 'text/plain'
		requestType = self.request.get('type')

		logging.info('Received request with type: ' + requestType)

		if requestType == 'delete':	
			eventName = self.request.get('name')

			if "_" in eventName:
				eventName = self.parseEventName(eventName)

			logging.info('Name of event to be deleted: ' + eventName)
			self.deleteEvent(eventName)

		else :
			if requestType == 'update':
				eventName = self.request.get('name')

				if "_" in eventName:
					eventName = self.parseEventName(eventName)

				logging.info('Name of event to be updated: ' + eventName)
				self.updateEvent(eventName)

	def parseEventName(self,unparsedEventName):
		eventName = re.sub('_',' ',unparsedEventName)
		return eventName
		