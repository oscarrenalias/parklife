from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.pinboard import pinboard
from app.dateutil.parser import *
import logging

class PinboardSource(Source):
    
    source_id = 'pinboard'
    
    FETCH_ALL_MAX_LINKS = 100
    
    def PinboardSource(self):
        pass
    
    #
    # generate a connection to the Pinboard API endpoint
    #    
    def __getConnection(self):
        return(pinboard.open(Config.getKey("pinboard_user"), Config.getKey("pinboard_password")))
    
    #
    # returns the Entry object point to the delicious link that was most recently fetched
    #    
    def getMostRecentLink(self):
        query = Entry.gql( 'WHERE source = :source ORDER BY created DESC', source=self.source_id)
        if query.count() == 0:
            return None
            
        # can you do this?
        return(query.fetch(1)[0])        
        
    def getAll(self):
        # fetches all pinboard links
        p = self.__getConnection()
        
        try:
            posts = p.posts(count=self.FETCH_ALL_MAX_LINKS)
        except: 
            # log the error but still throw the exception upwards
            logging.error( 'Could not retreive Pinboard posts for user: ' + str(Config.getKey('pinboard_user')))
            # re-raise the exception so that it can be processed upstream
            raise
        
        return posts
        
    def getLatest(self):
        
        latestLink = self.getMostRecentLink()
        if latestLink == None:
            # should we fetch them all?
            logging.debug( 'Fetching all pinboard links because there is none in the database')
            return self.getAll()

        logging.debug( 'Pinboard source: doing a delta update' )
        
        # check the date of the most recent link
        most_recent = self.getMostRecentLink()
        date = most_recent.created
        # and make a API call to obtain all the links since that one
        p = self.__getConnection()
                                
        logging.debug('Date of the most recent pinboard link is ' + str(most_recent.created))
        
        try:
            posts = p.posts(date=most_recent.created.strftime("%Y-%m-%dT%H:%M:%SZ"))
        except:
            logging.error( 'Could not retreive Pinboard posts for user: ' + str(Config.getKey('pinboard_user')))
            raise
        
        return posts
    
    def toEntry(self, post):
        e = Entry()
        e.external_id = post['hash']
        e.url = post['href']
        e.title = post['description']
        e.text = post['extended']
        e.source = self.source_id
        e.created = parse( post['time'] )
        e.tags = post['tags']
        
        return e