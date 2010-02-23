from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.dateutil.parser import *
from app.feedparser import feedparser
import logging

class GoogleReaderSource(Source):
	
	def GoogleReaderSource(self):
		self.source_id = 'googlereader'
	
	def getAll(self):		
		raise Exception('GoogleReaderSource::getAll() not implemented yet')
		
	def getLatest(self):

		feed_link = Config.getKey( 'google_reader_feed' )
		if feed_link == None:
			raise Exception( 'Please configure your Google Reader shared items feed first!' )
			
		response = feedparser.parse( feed_link )
		return self.__processEntries(response.entries)
			
	def __processEntries(self, entries):		
		# process all data received from delicious
		total = 0
		added = 0
		for entry in entries:
			total = total + 1
			if self.isDuplicate(entry.id, 'googlereader') == False:
				e = Entry()
				e.title = entry.title
				e.url = entry.link
				e.created = parse(entry.published)
				e.source = 'googlereader'
				e.external_id = entry.id
				# if there's an annotation, let's use it as the body for the post
				if 'content' in entry:
					if len(entry.content) > 1:
						e.text = entry.content[1].value
						
				e.put()
				
				added = added + 1
			else:
				logging.debug( 'Skipping link ' + post['hash'] + ' because it is duplicate')
		
		logging.debug('GoogleReaderSource.__processEntries(): Processed ' + str(total) + ' links, ' + str(added) + ' updated' )
		return added