from google.appengine.ext import webapp
from app.view.view import View

class BaseHandler(webapp.RequestHandler):
    def get(self):
        self.__notImplemented("GET")
    
    def post(self):
        self.__notImplemented("POST")
    
    def put(self):
        self.__notImplemented("PUT")
    
    def delete(self):
        self.__notImplemented("DELETE")
        
    def __notImplemented(self, method):
        self.error(500)
        self.response.out.write("Requested method %s not supported" % method)
        
    def writeResponse(self, template, data = {}):
        self.response.out.write(View(template, self.request).render(data))
