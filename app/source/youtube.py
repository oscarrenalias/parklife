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
	
	def YouTubeSource(self):
		self.source_id = 'youtube'
		
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
	
	def getAll(self):
		client = gdata.youtube.service.YouTubeService(client_id='Parklife', developer_key=Defaults.YOUTUBE_API_KEY)		
		gdata.alt.appengine.run_on_appengine(client)		
		
		# retrieve the favorites
		videos = client.GetYouTubeVideoFeed( self.getFeedUri( user=Config.getKey('youtube_user'), feed='favorites', count='11'))
		for video in videos.entry:

			if self.isDuplicate(video.id.text, 'youtube') == False:
				e = Entry()
				if video.title != None:
					e.title = video.title.text.decode('UTF-8')
				if video.content != None:
					e.text = video.content.text.decode('UTF-8')
				e.source = 'youtube'
				e.external_id = video.id.text
				e.created = parse( video.published.text )
			
				if video.media.keywords != None:
					tag_lst = video.media.keywords.text.split(',')
					e.tags = ' '.join(tag_lst)
				e.put()
			else:
				print 'video is duplicate: ' + video.id.text
		
	def getLatest(self):
		return self.getAll()
			
	def __processLinks(self, posts):		
		pass