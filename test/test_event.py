import unittest
import webapp2
from libraries import webtest
from google.appengine.api import memcache
from google.appengine.ext import db
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
            'description': "Description",
            'local': "Lisbon",
            'date': "2013-04-27",
            'time': "21:00",
            'facebook_link': "http://www.facebook.com"
        }

        response = self.testapp.post('/events/new', params)
        self.assertEqual(1, Event.all().count())
        


