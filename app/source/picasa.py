from app.source import Source
from app.models.config import Config
from app.models.entry import Entry
from app.dateutil.parser import *
from app.utils import Utils
from app.google import gdata
import app.google.gdata.photos.service
#import gdata.geo
import app.google.gdata.media
import logging

class PicasaSource(Source):
	
	def PicasaSource(self):
		self.source_id = 'picasa'
		
	def getAll(self):
		print 'PicasaSource.getAll not implemented'

	# 
	# return the Entry object with the newest Picasa entry
	# Returns None if none is found
	#
	def getLatestPicasaEntry(self):
		query = Entry.gql( 'WHERE source = :source ORDER BY created DESC', source='picasa')
		if query.count() == 0:
			return None
			
		# can you do this?
		return(query.fetch(1)[0])		

	def getLatest(self):

		# get latest entries only
		# retrieve the twitter user
		c = Config()
		picasa_user = c.getKey('picasa_user')
		
		# quit right away if no twitter user has been provided
		if picasa_user == None:
			raise Exception( 'Picasa username missing, unable to proceed' )
			
		# get the most recent picasa entry from the db
		latest_entry = self.getLatestPicasaEntry()
		if latest_entry == None:
			latest_entry_created_date = parse("2000-01-01T00:00:00.000Z")
		else:
			latest_entry_created_date = latest_entry.created
			
		# to hold the pictures to be added	
		to_add = []
			
		# get the latest pictures via the API
		client = gdata.photos.service.PhotosService()
		latest_pics = client.GetUserFeed(user=picasa_user, kind='photo', limit='50') # let's see if we can process so many of them
		for pic in latest_pics.entry:
			# is it newer than the newest picasa entry in the db?
			print pic.published.text
			if(parse(pic.published.text)) > latest_entry_created_date:
				to_add.append(pic)
			else:
				# we can probably get out of this loop
				break
				
		self._createEntry(to_add)
		
		logging.debug("to add: " + str(len(to_add)))
		
		return(len(to_add))
		
	def _createEntry(self, pictures):
		html = "<div class=\"picasa-entry\"><ul class=\"picasa-entry-ul\">"
		for pic in pictures:
			# build the markup
			html += '<li class=\"picasa-entry-li picasa-entry-picture\">\
					  <a href="%s" title="%s">\
			           <img class=\"picasa-entry-img\" src="%s" data:picasa-thumb72="%s" data:picasa-thumb144="%s" data:picasa-thumb288="%s" alt="%s" />\
			          </a>\
			         </li>' % (pic.GetHtmlLink().href, pic.title.text, pic.media.thumbnail[2].url, pic.media.thumbnail[0].url, pic.media.thumbnail[1].url, pic.media.thumbnail[2].url, pic.title.text)
		html += "</ul></div>"

		# and now create the entry
		c = Config()
		e = Entry(source = 'picasa',
			text = html,
			title = "%s new pictures in Picasa" % (str(len(pictures))),
			url = "http://picasaweb.google.com/" + c.getKey('picasa_user'))			
		e.put()			

	def getLastUpdateDate(self):
		print( 'getLastUpdateDate' )

	def getLastUpdateExternalId(self):
		print( 'getLastUpdateDate' )