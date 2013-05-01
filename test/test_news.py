import unittest
import webapp2
from libraries import webtest
from google.appengine.ext import testbed

from model.news import News
from controllers.NewsController import NewsController

class NewsTestCase(unittest.TestCase):

    def setUp(self):
        routes = [
            ('/news/new', NewsController.NewNewsHandler),
            (r'/news/(\d+)', NewsController.ShowNewsHandler),
            (r'/news/delete/(\d+)', NewsController.DeleteNewsHandler),
            (r'/news/edit/(\d+)', NewsController.EditNewsHandler),
            (r'/news/images/(\d+)', NewsController.ImageHandler)
        ]
        app = webapp2.WSGIApplication(routes=routes, debug=True)
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

    def tearDown(self):
        self.testbed.deactivate()


    def test_new_news(self):
        params = {
           'title': "Event",
           'short_description': "Short description",
           'description': "Description"
        }

        self.testapp.post('/news/new', params)
        self.assertEqual(1, News.all().count())

    def test_delete_news(self):
        news = News()
        news.put()
        self.assertEqual(1, News.all().count())
        
        path = "/news/delete/" + str(news.key().id())
        
        self.testapp.get(path)
        self.assertEqual(0, News.all().count())

    def test_show_news(self):
        news = News(title="News", short_description="Short Description", description="Description1")
        news.put()
        
        path = "/news/" + str(news.key().id())
        
        response = self.testapp.get(path)
        self.assertEqual(200, response.status_int)

    def test_edit_news(self):
        news = News(title="News", short_description="Short Description", description="Description1")
        news.put()
        ident = news.key().id()
        params = {
           'title': "News",
           'short_description': "Short Description",
           'description': "Description2"
        }
        
        path = "/news/edit/" + str(news.key().id())
        response = self.testapp.post(path, params)
        
        news = News.get_by_id(ident)
        
        self.assertEqual(1, News.all().count())
        self.assertEqual(302, response.status_int)
        self.assertEqual("Description2", str(news.description))




