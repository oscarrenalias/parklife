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
	
	# maximum amount of pictures to retrieve from picasa
	MAX_PHOTOS = '100'
	
	source_id = 'picasa'
	
	def PicasaSource(self):
		pass
		
	def getAll(self):
		raise NotImplementedError('PicasaSource.getAll not implemented')

	# 
	# return the Entry object with the newest Picasa entry
	# Returns None if none is found
	#
	def getLatestPicasaEntry(self):
		query = Entry.gql( 'WHERE source = :source ORDER BY created DESC', source=self.source_id)
		if query.count() == 0:
			return None
			
		return(query.fetch(1)[0])		

	def getLatest(self):
		# retrieve the user
		c = Config()
		picasa_user = c.getKey('picasa_user')		
		# quit right away if no user has been provided
		if picasa_user == None:
			raise Exception( 'Picasa username missing, unable to proceed' )
			
		# get the most recent picasa entry from the db
		latest_entry = self.getLatestPicasaEntry()
		if latest_entry == None:
			latest_entry_created_date = parse("2000-01-01T00:00:00")
		else:
			latest_entry_created_date = latest_entry.created
			
		# to hold the pictures to be added	
		to_add = []
			
		# get the latest pictures via the API
		client = gdata.photos.service.PhotosService()
		latest_pics = client.GetUserFeed(user=picasa_user, kind='photo', limit=self.MAX_PHOTOS) # let's see if we can process so many of them
		for pic in latest_pics.entry:
			# we don't need the time zone, and if we keep it then we'll run into trouble when comparing the dates
			picture_date = pic.published.text[0:len(pic.published.text)-5]
			logging.debug("Picasa source: latest_entry_created_date: %s - pic.published.text: %s - picture_date: %s" % (str(latest_entry_created_date), str(pic.published.text), str(picture_date)))			

			# is it newer than the newest picasa entry in the db?			
			if(parse(picture_date)) > latest_entry_created_date:
				to_add.append(pic)
			else:
				# we can probably get out of this loop
				break
				
		# create an entry only if there's something to add
		num_new_pics = len(to_add)
		
		# this should will ever only add one entry, regardless of how many pictures are found		
		logging.debug("Picasa source: new pictures to be added: " + str(num_new_pics))
		data = []
		if(num_new_pics > 0):
			data.insert(0, to_add)
								
		return(data)
	
	def pictureHTML(self, pic, isMultiple):
		html = ""
		
		if isMultiple == True:
			html += '<li class=\"picasa-entry-li picasa-entry-picture\">'
			
		html += '<a href="%s" title="%s">\
			       <img class="picasa-entry-img" src="%s" data:picasa-thumb72="%s" data:picasa-thumb144="%s" data:picasa-thumb288="%s" alt="%s" /> \
			     </a>' % (pic.GetHtmlLink().href, pic.title.text, pic.media.thumbnail[2].url, pic.media.thumbnail[0].url, pic.media.thumbnail[1].url, pic.media.thumbnail[2].url, pic.title.text)
			
		if isMultiple == True:
			html += '</li>'
			
		return(html)			
	
	def toEntry(self, pictures):
		# and now create the entry
		c = Config()
		e = Entry(source = self.source_id,
			url = "http://picasaweb.google.com/" + c.getKey('picasa_user'))
		
		# define whether we show a matrix with pictures (in case we've got more than one) or just a bigger thumbnail)
		if(len(pictures) > 1):
			html = "<div class=\"picasa-entry\">"
			html += "<ul class=\"picasa-entry-ul\">"
			#for pic in pictures:
			#	html += self.pictureHTML(pic, True)
			html += "".join(map(lambda e: self.pictureHTML(e, True), pictures))				
			html += "</ul></div>"

			e.text = html			
			e.title = "%s new photos (%s)" % (str(len(pictures)), self._getTodayDate())
		else:
			pic = pictures.pop()
			# only one picture, we can show a bigger version of the picture
			# the markup uses different CSS classes so that we can control the styling separately
			e.title = "New photo upload (%s)" % (self._getTodayDate())
			e.text = "<div class=\"picasa-single-entry\">" + self.pictureHTML(pic, False) + "</div>"
					
		return e
		
	#
	# returns today's date in a nicely formatted string
	# @private
	#
	def _getTodayDate(self):
		import datetime
		return(datetime.datetime.now().strftime("%d-%m-%Y"))