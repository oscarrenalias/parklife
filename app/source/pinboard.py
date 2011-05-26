from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.pinboard import pinboard
from app.dateutil.parser import *
from defaults import Defaults
import logging

class PinboardSource(Source):
    
    source_id = 'pinboard'
    
    FETCH_ALL_MAX_LINKS = 100
    
    def PinboardSource(self):
        pass
    
    def getLatest(self):        
        most_recent = self.getMostRecentEntry()
        try:
            p = pinboard.open(Config.getKey("pinboard_user"), Config.getKey("pinboard_password"))            
            if most_recent == None:                
                posts = p.posts(count=self.FETCH_ALL_MAX_LINKS)
            else:
                posts = p.posts(date=most_recent.created.strftime("%Y-%m-%dT%H:%M:%SZ"))
        except:
            logging.error( 'Could not retrieve Pinboard posts for user: ' + str(Config.getKey('pinboard_user')))
            raise
        
        # filter posts whose title is "instagram"
        if Defaults.PINBOARD_IGNORE_INSTAGRAM_LINKS == True:
            logging.debug("Filtering Instagram posts")
            posts = filter(lambda p: p['description'].lower() != 'instagram', posts)
        
        return posts
    
    def toEntry(self, post):
        e = Entry()
        e.external_id = post['hash']
        e.url = post['href']
        e.title = post['description']
        e.text = post['extended']
        e.source = self.source_id
        e.created = parse( post['time'] )
        # this is a bit weird but for some reason, the list of tags from post['tags'] will
        #Êreport at least one element even if it's empty, so we need to protect against that
        e.tags = [] if len(post['tags'][0]) == 0 else post['tags']
        
        return e