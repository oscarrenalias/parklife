from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.dateutil.parser import *
from app.feedparser import feedparser
import logging

class GoogleReaderSource(Source):
	
	source_id = 'googlereader'
	
	def GoogleReaderSource(self):
		pass
	
	def getLatest(self):
		feed_link = Config.getKey( 'google_reader_feed' )
		if feed_link == None:
			raise Exception( 'Please configure your Google Reader shared items feed first!' )
			
		response = feedparser.parse( feed_link )
		return response.entries
	
	def toEntry(self, item):
		e = Entry()
		e.title = item.title
		e.url = item.link
		e.created = parse(item.published)
		e.source = self.source_id
		e.external_id = item.id
		# if there's an annotation, let's use it as the body for the post
		if 'content' in item:
			if len(item.content) > 1:
				e.text = item.content[1].value
		
		return e