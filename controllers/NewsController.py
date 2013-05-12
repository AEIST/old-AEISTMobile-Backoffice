#!/usr/bin/python

import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import images
from model.news import News

import os
from datetime import datetime

class NewsController(webapp2.RequestHandler):

    @staticmethod
    def getTemplate(path):
        jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace('controllers','')))
        return jinja_environment.get_template(path)

    def get(self):
        news = getAllNews(self)
        templateValues = {
            'news': news
        }

        template = NewsController.getTemplate('templates/news/news.html')
        self.response.out.write(template.render(templateValues))

    class NewNewsHandler(webapp2.RequestHandler):

        def get(self):
            template = NewsController.getTemplate('templates/news/new_news.html')
            self.response.out.write(template.render({}))

        def post(self):
            news = News()
            news.title = self.request.get("title")
            news.short_description = self.request.get("short_description")
            news.description = self.request.get("description")
            news.created_at = datetime.now().date()

            if self.request.get("image"):
                news.image = db.Blob(images.resize(self.request.get("image"), 300))

            news.put()
            self.redirect("/news")

    class ShowNewsHandler(webapp2.RequestHandler):

        def get(self, *args):
            news = getNews(args[0])
            template = NewsController.getTemplate('templates/news/show_news.html')
            self.response.out.write(template.render(news))

    class DeleteNewsHandler(webapp2.RequestHandler):

        def get(self, *args):
            news = News.get_by_id(long(args[0]))

            if news:
                news.delete()

            self.redirect('/news')

    class EditNewsHandler(webapp2.RequestHandler):

        def get(self, ident):
            news = getNews(ident)
            template = NewsController.getTemplate('templates/news/edit_news.html')
            self.response.out.write(template.render(news))

        def post(self, ident):
            news = News.get_by_id(long(ident))
            news.title = self.request.get("title")
            news.short_description = self.request.get("short_description")
            news.description = self.request.get("description")

            if self.request.get("image"):
                news.image = db.Blob(images.resize(self.request.get("image"), 300))

            db.put(news)
            self.redirect("/news")

    class ImageHandler(webapp2.RequestHandler):

        def get(self, ident):
            news = News.get_by_id(long(ident))

            if news.image:
                self.response.headers['Content-Type'] = 'image/*'
                self.response.out.write(news.image)


def getAllNews(self):
    query = News.all().order("-created_at")
#     query = db.GqlQuery("SELECT * FROM News")
    news = []

    for n in query:

        jsonEventInfo = {}
        jsonEventInfo['title'] = n.title
        jsonEventInfo['short_description'] = n.short_description
        jsonEventInfo['description'] = n.description
        jsonEventInfo['date'] = n.created_at.strftime('%d-%m-%Y')
        
        currentUrl = self.request.url;

        jsonEventInfo['delete_link'] = currentUrl + '/delete/' + str(n.key().id())
        jsonEventInfo['edit_link'] = currentUrl + '/edit/' + str(n.key().id())
        jsonEventInfo['direct_link'] = currentUrl + '/' + str(n.key().id())
        news.append(jsonEventInfo)

    return news


def getNews(ident):
    news = News.get_by_id(long(ident))

    jsonEventInfo = {}
    jsonEventInfo['title'] = news.title
    jsonEventInfo['short_description'] = news.short_description
    jsonEventInfo['description'] = news.description
    
    if news.image:
        jsonEventInfo['image_link'] = '/news/images/' + str(ident)

    news = jsonEventInfo
    return news

