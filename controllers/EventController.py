#!/usr/bin/python

from google.appengine.ext import webapp

import json
import logging

#TODO: put all the controller event logic in this class!!
class EventController(webapp.RequestHandler):


	def get(self, *args):

			event_name = self.request.get("name")
			self.response.headers['Content-Type'] = 'text/plain'
			test = {}
			test['xpto'] = 'delta' + event_name
			json_str = json.dumps(test)
			self.response.out.write(json_str)	

