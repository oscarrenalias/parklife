from source import Source
from models.config import Config
from models.entry import Entry
from dateutil.parser import *
from app.instagram.client import InstagramAPI
from defaults import Defaults
import logging

#
# Source class that reads data from Instagram
#
class InstagramSource(Source):
    
    source_id = 'instagram'

    MAX_ITEMS = 100
    
    def InstagramSource(self):
        pass 
    
    def getAPI(self):
        access_token = Config.getKey( 'instagram_token' )
        if access_token == None:
            raise Exception( 'Please provide a valid Instagram access token before executing this source' )
            
        return InstagramAPI(access_token=access_token)
    
    def getLatest(self):        
        mostRecentEntry = self.getMostRecentEntry()

        api = self.getAPI()
        
        if mostRecentEntry == None:
            pictures = api.user_recent_media(count=self.MAX_ITEMS)[0]
        else:
            pictures = api.user_recent_media(count=self.MAX_ITEMS)[0]

        return pictures
    
    #
    # builds the markup for the instagram posts
    #
    def makeInstagramText(self, picture):
        html = '<div class="instagram-entry"> \
                <a class="instagram-entry-link" href="%s"><img class="instagram-entry-img" alt="%s" src="%s" /></a> \
                </div>' % (picture.link, picture.caption.text, picture.images[Defaults.INSTAGRAM_IMAGE_SIZE].url)
                
        return(html)            
    
    def toEntry(self, item):
        e = Entry()
        e.external_id = item.id 
        e.created = item.created_time
        e.source = self.source_id
        e.url = item.link
        e.title = item.caption.text
        e.text = self.makeInstagramText(item)
        
        # save the location data in case it's got any
        if 'location' in dir(item):
            e.lat = "%.15f" % item.location.point.latitude
            e.lng = "%.15f" % item.location.point.longitude
            e.location_name = item.location.name
        
        return e