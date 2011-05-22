from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.pinboard import pinboard
from app.dateutil.parser import *
import logging

PINBOARD_SOURCE_NAME = 'pinboard'

class PinboardSource(Source):
    
    def PinboardSource(self):
        self.source_id = PINBOARD_SOURCE_NAME
    
    #
    # generate a connection to the Pinboard API endpoint
    #    
    def __getConnection(self):
        return(pinboard.open(Config.getKey("pinboard_user"), Config.getKey("pinboard_password")))
    
    #
    # returns the Entry object point to the delicious link that was most recently fetched
    #    
    def getMostRecentLink(self):
        query = Entry.gql( 'WHERE source = :source ORDER BY created DESC', source=PINBOARD_SOURCE_NAME)
        if query.count() == 0:
            return None
            
        # can you do this?
        return(query.fetch(1)[0])        
        
    def getAll(self):
        # fetches all pinboard links
        p = self.__getConnection()
        
        try:
            posts = p.posts(count=100)
        except: 
            # log the error but still throw the exception upwards
            logging.error( 'Could not retreive Pinboard posts for user: ' + str(Config.getKey('pinboard_user')))
            # re-raise the exception so that it can be processed upstream
            raise
        
        total = self.__processLinks(posts)
        
        logging.debug( 'Pinboard updated ' + str(total) + ' links' )
        
        return total
        
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
        posts = p.posts(date=most_recent.created.strftime("%Y-%m-%dT%H:%M:%SZ"))
        
        return self.__processLinks(posts)
            
    def __processLinks(self, posts):        
        # process all data received from delicious
        total = 0
        added = 0
        for post in posts['posts']:
            total = total + 1
            if self.isDuplicate(post['hash'], PINBOARD_SOURCE_NAME) == False:
                # only persist if not duplicate
                e = Entry()
                e.external_id = post['hash']
                e.url = post['href']
                e.title = post['description']
                e.text = post['extended']
                e.source = PINBOARD_SOURCE_NAME
                e.created = parse( post['time'] )
                if post['tags'] != '':
                    e.tags = post['tags'].split(' ')    
                else:
                    e.tags = []
                
                e.put()
                
                added = added + 1
            else:
                logging.debug( 'Pinboard source: Skipping link ' + post['hash'] + ' because it is duplicate')
        
        logging.debug('Pinboard source: processed ' + str(total) + ' links, ' + str(added) + ' updated' )
        return added