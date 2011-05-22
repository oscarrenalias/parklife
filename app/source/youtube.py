from app.source import Source
from app.google import gdata
from app.google.gdata import youtube
from app.google.gdata.youtube import service
from app.google.gdata.alt import appengine
from app.models.config import Config
from app.models.entry import Entry
from app.dateutil.parser import *
from defaults import Defaults
import logging

class YouTubeSource(Source):
	
	source_id = 'youtube'
	
	FETCH_ALL_MAX_ITEMS = 20
	
	def YouTubeSource(self):
		pass
		
	def getFeedUri(self, **params):
		uri = 'http://gdata.youtube.com/feeds/api/users/' + params['user']
		if params['feed'] != None:
			uri = uri + '/' + params['feed']
		if params['count'] != None:
			uri = uri + '?max-results=' + params['count']
			
		return uri
	
	def getFlashPlayerHTML(self, url):
		code = '<object width="425" height="350"> \
		       <param name="movie" value="' + url + '"></param> \
		       <embed src="' + url + '" type="application/x-shockwave-flash" \
		       width="425" height="350"></embed></object>'

		return code
	
	#
	# Returns true if the video can be saved
	#
	def isValid(self, video):
		if video.content != None:
			if video.media.content != None:
				return True
		
		return False
			
	def toEntry(self, video):
		e = Entry()
		if video.title != None:
			e.title = video.title.text.decode('UTF-8')
		if video.content != None:
			if video.media.content != None:
				e.text = '<div class="video">' + self.getFlashPlayerHTML( video.media.content[0].url ) + '</div>' 
			if video.content.text != None:
				e.text += video.content.text.decode('UTF-8')

		e.source = self.source_id
		e.external_id = video.id.text
		e.created = parse( video.published.text )
		e.url = video.link[0].href
	
		if video.media.keywords != None:
			# split the tags 
			e.tags = video.media.keywords.text.decode('UTF-8').replace(' ','').split(',')
			
			
		# save the location data if available
		if video.geo:
			e.lat = str(video.geo.latitude())
			e.lng = str(video.geo.longitude())
			
		return e
	
	def getAll(self):
		client = gdata.youtube.service.YouTubeService(client_id='Parklife', developer_key=Defaults.YOUTUBE_API_KEY)		
		gdata.alt.appengine.run_on_appengine(client)		
		
		# retrieve the favorites
		favorites = client.GetYouTubeVideoFeed( self.getFeedUri( user=Config.getKey('youtube_user'), feed='favorites', count=str(self.FETCH_ALL_MAX_ITEMS)))
		# and the uploaded
		uploaded = client.GetYouTubeVideoFeed( self.getFeedUri( user=Config.getKey('youtube_user'), feed='uploads', count=str(self.FETCH_ALL_MAX_ITEMS)))

		# merge the arrays after we've verified that all videos are valid and should be returned
		videos = filter(self.isValid, favorites.entry) + filter(self.isValid, uploaded.entry)
		
		return videos
		
	def getLatest(self):
		return self.getAll()