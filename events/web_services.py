'''
Created on Oct 29, 2012

@author: joaovasques
'''

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext import blobstore
import json
import base64
from protorpc import messages
from model.event import Evento

class EventInformation(messages.Message):
    nome = messages.StringField(1)
    descricao = messages.StringField(2)
    link_facebook = messages.StringField(3)
    image_key = messages.StringField(5)
    eventTag = messages.StringField(4)
    image_base_64 = messages.StringField(6)

'''
Gets information about a specific event given key (name)

Information (JSON object) -> EventInformation
''' 
class GetEventInformation(webapp.RequestHandler):
    
    def get(self, *args):
        
        # Get event name from HTTP argument
        event_name = str(self.request.get_all("name")[0])             
        event_name = event_name.replace("_", " ")           
          
        self.response.headers['Content-Type'] = 'application/json'         
        query = db.GqlQuery("SELECT * "
                            "FROM Evento")

        #event = EventInformation(nome='nome-def',descricao='descricao-def',link_facebook='link_-def')
        event = Evento()
        event_info = {}
        
        for event in query:
            e = event            
            name = e.nome
            des = e.descricao
            link = e.link_facebook
            image_key = e.imagem_key                       
        
            if name == event_name:
                
                event_info['name'] = str(name)
                event_info['description'] = str(des)
                event_info['facebook_link'] = str(link)
                event_info['author'] = e.author
                #event_info['eventTag'] = e.eventTag
                event_info['image'] = base64.b64encode(str(e.image))

                #TODO: put binary into string -> base64 -> put into json array
#                 event_info['image_key'] = str(image_key)
#                 image_reader = blobstore.BlobReader(image_key)
#                 image = image_reader.read()                
#                 event_info['image'] = image                
                break
            
        json_event_info = json.dumps(event_info)    
        self.response.out.write(json_event_info)
        

'''
Gets a list (JSON array) with the names of all events
'''
class GetAllEventsNames(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        
        query = db.GqlQuery("SELECT * "
                            "FROM Evento")      
        events = []
                
        for n in query:
            
            json_event_info = {}            
            name = n.nome                      
            json_event_info['name'] = name         
            events.append(json_event_info)
                    
        r = {}
        r['events_names'] = events
        r = json.dumps(r)        
        self.response.out.write(r)          
        

'''
Returns a list (JSON array) with information about all events
'''        
class ShowAllEvents(webapp.RequestHandler):
    
    def get(self, *args):
        
        self.response.headers['Content-Type'] = 'application/json'
        
        query = db.GqlQuery("SELECT * "
                            "FROM Evento")      
        events = []
                
        for n in query:
            
            json_event_info = {}
            
            name = n.nome
            des = n.descricao
            link = n.link_facebook
            image_key = n.imagem_key
            
            json_event_info['name'] = str(name)
            json_event_info['description'] = str(des)
            json_event_info['facebook_link'] = str(link)
            json_event_info['image_key'] = str(image_key)          
            events.append(json_event_info)
            
        
        response = json.dumps(events)
        self.response.out.write(response) 
