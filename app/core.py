import webapp2
from app.view.view import View
from defaults import Defaults
from app.pager.pagedquery import PagedQuery
from app.models.entry import Entry

class BaseHandler(webapp2.RequestHandler):
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
        
    def writeResponse(self, template, data = {}, force_renderer=None):
        responseContent, contentType = View(template, self.request).render(data)
        self.response.headers['Content-type'] = contentType
        self.response.out.write(responseContent)

    def getCurrentPage(self):
        try:
            page = int(self.request.get( 'p' ))
        except ValueError:
            page = 1
            
        return page

    # shortcut method for retrieving a bunch of entries given a default filter    
    def getEntryQuery(self, extraFilters = {}):        
        return Entry.getPagedQueryWithBasicFilters(extraFilters)