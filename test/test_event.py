#coding=utf-8

import unittest
import webapp2
from libraries import webtest
from google.appengine.ext import testbed

from model.event import Event
from controllers.EventController import EventController

class EventTestCase(unittest.TestCase):

	def setUp(self):
		routes = [
			('/events', EventController),
			('/events/new', EventController.NewEventHandler),
			(r'/events/(\d+)', EventController.ShowEventHandler),
			(r'/events/delete/(\d+)', EventController.DeleteEventHandler),
			(r'/events/edit/(\d+)', EventController.EditEventHandler),
			(r'/events/images/(\d+)', EventController.ImageHandler)
		]
		app = webapp2.WSGIApplication(routes=routes, debug=True)
		self.testapp = webtest.TestApp(app)
		self.testbed = testbed.Testbed()
		self.testbed.activate()

	def tearDown(self):
		self.testbed.deactivate()


	def test_new_event(self):
		params = {
			'name': "Event",
			'description': "Descrição",
			'location': "Lisbon",
			'date': "2013-04-27",
			'time': "21:00",
			'facebook_link': "http://www.facebook.com"
		}

		self.testapp.post('/events/new', params)

		results = Event.all().fetch(1, 0)
		event = results[0]

		self.assertEqual(1, Event.all().count())
		self.assertEqual("Event", event.name)
		self.assertEqual(u"Descrição", event.description)
		self.assertEqual("Lisbon", event.location)
		self.assertEqual("2013-04-27", event.date)
		self.assertEqual("21:00", event.time)
		self.assertEqual("http://www.facebook.com", event.linkFacebook)

	def test_delete_event(self):
		event = Event()
		event.put()
		self.assertEqual(1, Event.all().count())

		path = "/events/delete/" + str(event.key().id())

		self.testapp.get(path)
		self.assertEqual(0, Event.all().count())

	def test_show_event(self):
		event = Event()
		event.put()

		path = "/events/" + str(event.key().id())

		response = self.testapp.get(path)
		self.assertEqual(200, response.status_int)

	def test_edit_event(self):
		event = Event(name="Event", description="Description1", location="Lisbon", date="2013-04-28", time="13:00", linkFacebook="http://www.facebook.com")
		event.put()
		ident = event.key().id()
		params = {
			'name': "New event",
			'description': "Description2",
			'location': "Porto",
			'date': "2013-04-28",
			'time': "22:00",
			'facebook_link': "http://www.google.com"
		}

		path = "/events/edit/" + str(event.key().id())
		response = self.testapp.post(path, params)

		event = Event.get_by_id(ident)

		self.assertEqual(1, Event.all().count())
		self.assertEqual(302, response.status_int)
		self.assertEqual("New event", event.name)
		self.assertEqual("Description2", event.description)
		self.assertEqual("Porto", event.location)
		self.assertEqual("2013-04-28", event.date)
		self.assertEqual("22:00", event.time)
		self.assertEqual("http://www.google.com", event.linkFacebook)




